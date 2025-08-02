[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/r7JSDOZA)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=19964283&assignment_repo_type=AssignmentRepo)


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
