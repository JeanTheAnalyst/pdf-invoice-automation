# pdf-invoice-automation
Automating PDF invoice and packing list processing using Python

# PDF Invoice Automation

## Overview
This project automates the extraction and processing of data from commercial invoices and packing lists in PDF format.

## Features
- Extracts structured data from PDFs using pdfplumber
- Cleans and processes data using pandas
- Uses regex to identify key business fields (PO, description, heat number, skid)
- Merges invoice and packing list data
- Generates Excel reports for receiving operations
- Supports batch processing of multiple files

## Tech Stack
- Python
- pdfplumber
- pandas
- regex

## Business Value
This tool reduces manual data entry, improves accuracy, and speeds up reporting workflows in supply chain operations.

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Place PDF files in the project folder

3. Run the script:
   python src/pdf_processor.py

## Sample Data
Example PDF files are available in the `sample_data/` folder for testing purposes.
