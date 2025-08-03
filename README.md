

# 📊 Apple Financial Statement Extractor & Visualizer

This Python project extracts key financial data from Apple's quarterly financial statement PDF and transforms it into clean, structured Excel files. It also generates insightful visualizations saved as a single PNG image.

---

## 🔍 Features

- ✅ **PDF Parsing** using `pdfplumber`
- 🧹 **Cleans and extracts** monetary data using regex
- 📑 **Identifies and segments** data into:
  - Statements of Operations
  - Balance Sheets
  - Statements of Cash Flows
  - Net Sales by Reportable Segment
  - Net Sales by Product Category
- 📊 **Summary statistics** (mean and median) for financial metrics
- 🧾 **Exports to Excel**:
  - `apple_financials_clean.xlsx` – Full detailed export
  - `apple_financials_minimal.xlsx` – Cleaned, analysis-ready export
- 📈 **Visualizations using Matplotlib**:
  - Net sales by segment
  - Net sales by product category
  - Balance sheet snapshot (Assets, Liabilities, Equity)
- 🖼️ **Saves a combined PNG** image of all charts:
  - `financial_analysis_visualizations.png`

---

## 🗂️ Output Files

| File Name                         | Description                                 |
|----------------------------------|---------------------------------------------|
| `apple_financials_clean.xlsx`    | Full export with parsed and raw values      |
| `apple_financials_minimal.xlsx`  | Clean labels and numeric values only        |
| `financial_analysis_visualizations.png` | Combined visualization of 3 charts   |

---

## 📦 Requirements

Install dependencies via pip:

```bash
pip install pdfplumber pandas numpy matplotlib openpyxl
