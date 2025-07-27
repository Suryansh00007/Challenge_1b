#  Challenge 1B: Persona-Driven Document Intelligence

##  Overview

This project is a scalable solution for **persona-based document intelligence**.  
It processes collections of PDFs and intelligently extracts the most relevant **sections** and **refined sub-sections**, based on:
- a defined **persona** (e.g., HR, Analyst, Travel Planner)
- a clear **task or job-to-be-done** (e.g., trip planning, form creation, recipe selection)

It supports multilingual documents and automatically creates input and output JSON files in the desired schema.

---

##  What It Does

For every `collectionXXX` folder:
- Reads PDFs from the `/PDFs/` subdirectory.
- Generates:
  -  `challenge1b_input.json`: contains challenge metadata and persona info.
  -  `challenge1b_output.json`: contains top relevant sections and sub-sections from the PDFs.

### Output Includes:
- Top 5 **Section Titles** (10–20 words) per document.
- Top 5 **Refined Paragraphs** (40+ words) per document.

Both are tagged with:
- `document` (filename),
- `page_number`,
- `importance_rank` (for sections).

---

##  Libraries Used

| Library       | Purpose |
|---------------|---------|
| `os`          | File/directory navigation. |
| `json`        | JSON file creation and parsing. |
| `fitz` (PyMuPDF) | PDF parsing and text extraction. |
| `datetime`    | Timestamping output JSONs. |

Install required packages with:

```bash
pip install PyMuPDF
