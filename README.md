PDF Invoice Automation
Overview

This project automates the extraction and processing of data from commercial invoices and packing lists in PDF format.

In real business operations, manually entering invoice data into Excel is time-consuming and error-prone. This tool replaces manual work with an automated data pipeline.

Workflow
Read PDF invoices and packing lists
Extract structured data using pdfplumber
Parse key fields using regex (PO, description, heat, skid)
Clean and transform data using pandas
Merge datasets and calculate unit cost
Generate structured Excel reports
Features
Automated PDF-to-Excel workflow
Batch processing by purchase order
Data cleaning and normalization
Regex-based field extraction
End-to-end data pipeline
Tech Stack
Python
pdfplumber
pandas
regex
Business Value
Reduces manual data entry
Improves accuracy and consistency
Saves significant processing time
Enables scalable document processing
How to Run
pip install -r requirements.txt
python src/pdf_processor.py
Sample Data

Example PDF files are available in the sample_data/ folder.

## Output Example

The script generates structured Excel files for receiving operations, including:
- PO number
- Description
- Quantity
- Heat Number
- Skid Number
