import pdfplumber
import re
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

PDF_PATH   = Path('apple_statement.pdf')    # Path of the PDF File for the statement - apple financial statement     
FULL_XLSX  = Path('apple_financials_clean.xlsx')
MIN_XLSX   = Path('apple_financials_minimal.xlsx') 

# Load and Extract data using pdfplumber
with pdfplumber.open(PDF_PATH) as pdf:
    raw_lines = []
    for p in pdf.pages:
        text = p.extract_text() or ""
        raw_lines += [ln.strip() for ln in text.splitlines()]

# Clean raw text and remove symbols
clean_lines = []
for ln in raw_lines:
    ln = ln.replace('!', '$')  
    ln = ln.replace('’', "'").replace('—', '-').replace('\u2014', '-')
    ln = re.sub(r'\s{2,}', ' ', ln)
    clean_lines.append(ln.strip())

# Regex: large numbers and include () negatives and put a -
BIG_NUM_RE = re.compile(r'\(?-?(?:\d{1,3}(?:,\d{3})+|\d{4,})(?:\.\d+)?\)?')

def parse_line(line: str):
    nums = BIG_NUM_RE.findall(line)
    if len(nums) >= 2:
        first_span = BIG_NUM_RE.search(line).span()
        label = line[:first_span[0]].strip(': ').strip()
        return label, nums[:2]
    return None

rows = []
for idx, ln in enumerate(clean_lines):
    res = parse_line(ln)
    if not res:
        continue
    label, nums = res

    def to_float(x: str) -> float:
        x = x.replace(',', '')
        neg = x.startswith('(') and x.endswith(')')
        if neg:
            x = x[1:-1]
        return -float(x) if neg else float(x)

    v1, v2 = map(to_float, nums[:2])
    rows.append({'line_idx': idx, 'label': label, 'value_1': v1, 'value_2': v2, 'raw': ln})

all_df = pd.DataFrame(rows)

# Finding section boundaries for easier parsing
def find_idx(keyword: str):
    hits = [i for i, l in enumerate(clean_lines) if keyword.lower() in l.lower()]
    if not hits:
        raise ValueError(f"Section header not found: {keyword}")
    return hits[0]

sections = {
    'operations'    : find_idx('STATEMENTS OF OPERATIONS'),
    'balance_sheet' : find_idx('BALANCE SHEETS'),
    'cash_flows'    : find_idx('STATEMENTS OF CASH FLOWS'),
    'segment_sales' : find_idx('Net sales by reportable segment'),
    'category_sales': find_idx('Net sales by category'),
}

def slice_df(start, end=None):
    if end is None:
        end = 10**9
    return all_df[(all_df.line_idx >= start) & (all_df.line_idx < end)].copy()

ops_df = slice_df(sections['operations'], sections['balance_sheet'])
bs_df  = slice_df(sections['balance_sheet'], sections['cash_flows'])
cf_df  = slice_df(sections['cash_flows'])

seg_df = slice_df(sections['segment_sales'], sections['category_sales'])
cat_df = slice_df(sections['category_sales'], sections['balance_sheet'])

# Standardising labels and handling missing values
def clean_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['label_clean'] = (df['label']
        .str.replace(r'[\$\(\)\d]+', '', regex=True)
        .str.replace(r'[^A-Za-z/& ]', '', regex=True)
        .str.strip().str.lower()
        .str.replace(r'[ /]+', '_', regex=True)
    )
    df = df.drop_duplicates(subset='label_clean')
    df[['value_1', 'value_2']] = df[['value_1', 'value_2']].fillna(0.0)
    return df

ops_df = clean_labels(ops_df)
bs_df  = clean_labels(bs_df)
cf_df  = clean_labels(cf_df)
seg_df = clean_labels(seg_df)
cat_df = clean_labels(cat_df)

# Divide into stats 
def stats(df: pd.DataFrame, name: str) -> pd.DataFrame:
    out = df[['value_1', 'value_2']].describe().loc[['mean', '50%']].rename(index={'50%': 'median'})
    out['statement'] = name
    return out

summary_all = pd.concat([
    stats(ops_df, 'operations'),
    stats(bs_df,  'balance_sheet'),
    stats(cf_df,  'cash_flows')
])

for d in (seg_df, cat_df):
    d['pct_change'] = (d['value_1'] - d['value_2']) / d['value_2'] * 100

# Export to Excel
with pd.ExcelWriter(FULL_XLSX) as writer:
    ops_df.to_excel(writer, sheet_name='operations', index=False)
    bs_df.to_excel(writer,  sheet_name='balance_sheet', index=False)
    cf_df.to_excel(writer,  sheet_name='cash_flows', index=False)
    seg_df.to_excel(writer, sheet_name='segment_sales', index=False)
    cat_df.to_excel(writer, sheet_name='category_sales', index=False)
    summary_all.to_excel(writer, sheet_name='summary_stats')

print(f"Saved full workbook to {FULL_XLSX.resolve()}")

# Minimal Financials Report export to excel 
keep = ['label_clean', 'value_1', 'value_2']
ops_f = ops_df[keep].assign(statement='operations')
bs_f  = bs_df[keep].assign(statement='balance_sheet')
cf_f  = cf_df[keep].assign(statement='cash_flows')
seg_f = seg_df[keep].assign(statement='segment_sales')
cat_f = cat_df[keep].assign(statement='category_sales')
all_min = pd.concat([ops_f, bs_f, cf_f, seg_f, cat_f], ignore_index=True)

with pd.ExcelWriter(MIN_XLSX) as writer:
    ops_f.to_excel(writer, sheet_name='operations', index=False)
    bs_f.to_excel(writer,  sheet_name='balance_sheet', index=False)
    cf_f.to_excel(writer,  sheet_name='cash_flows', index=False)
    seg_f.to_excel(writer, sheet_name='segment_sales', index=False)
    cat_f.to_excel(writer, sheet_name='category_sales', index=False)
    all_min.to_excel(writer, sheet_name='all', index=False)

print(f"Saved minimal workbook to {MIN_XLSX.resolve()}")

# Visualisations
fig, axs = plt.subplots(3, figsize=(10, 15)) #Combine all the plots into a single png

# Net sales by reportable segment
x1 = np.arange(len(seg_df))
axs[0].bar(x1 - 0.2, seg_df['value_1'], width=0.4, label='Q1 2024 (Dec 30, 2023)')
axs[0].bar(x1 + 0.2, seg_df['value_2'], width=0.4, label='Q1 2023 (Dec 31, 2022)')
axs[0].set_xticks(x1)
axs[0].set_xticklabels(seg_df['label'], rotation=45, ha='right')
axs[0].set_ylabel('Net Sales (USD millions)')
axs[0].set_title('Net Sales by Reportable Segment')
axs[0].legend()

# Net sales by product category
x2 = np.arange(len(cat_df))
axs[1].bar(x2 - 0.2, cat_df['value_1'], width=0.4, label='Q1 2024')
axs[1].bar(x2 + 0.2, cat_df['value_2'], width=0.4, label='Q1 2023')
axs[1].set_xticks(x2)
axs[1].set_xticklabels(cat_df['label'], rotation=45, ha='right')
axs[1].set_ylabel('Net Sales (USD millions)')
axs[1].set_title('Net Sales by Product Category')
axs[1].legend()

# Balance sheet snapshot
bs_tot = bs_df[bs_df['label_clean'].isin(
    ['total_assets', 'total_liabilities', 'total_shareholders_equity']
)].copy()
axs[2].bar(['Assets', 'Liabilities', 'Equity'], bs_tot['value_1'])
axs[2].set_ylabel('USD millions')
axs[2].set_title('Balance Sheet (Dec 30, 2023)')

plt.tight_layout()
plt.savefig('financial_analysis_visualizations.png') #Saving the png of the visualisations
plt.show()
