# pdf-OCR-to-txt

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chayne-wild/pdf-OCR-to-txt/blob/main/pdf_OCR_to_txt.ipynb)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)

A lightweight Optical Character Recognition (OCR) utility designed to convert image-based or scanned PDF documents into plain text (`.txt`) files. 

Built primarily for **Google Colaboratory** (and adaptable to local Linux/macOS/Windows environments), this tool rasterizes PDF pages at 300 DPI using `poppler` (`pdf2image`) and extracts text via Google's `Tesseract-OCR` engine (`pytesseract`).

---

## Key Features

* **Two-Stage Execution for Speed:** Dependency installation (`00_install_dependencies.py`) is separated from document conversion (`01_upload_and_convert.py`). You install the system binaries once per session, and then run the conversion script as many times as needed with zero setup overhead.
* **Collision-Proof Timestamped Outputs:** Output files are dynamically named using the original PDF filename and a precise execution timestamp (`<filename>_ocr_YYYYMMDD_HHMMSS.txt`). Uploading multiple PDFs simultaneously, or running the same document twice after tweaking OCR parameters, will never overwrite your previous outputs.
* **Flexible Deployment:** Launch directly in your browser with one click via the included Jupyter Notebook (`pdf_OCR_to_txt.ipynb`), or copy-paste the standalone `.py` scripts into your own workflow.

---

## When to Use This Tool

* **Best For:** Non-selectable, image-based PDFs, archival scans, photocopies, historical documents, and flattened PDFs where standard text extraction fails.
* **Not Needed For:** Digitally native PDFs where text is already selectable and searchable (lightweight parsers like `pypdf` or `pdfplumber` can extract embedded text layers directly without OCR).

---

## Quick Start

### Option 1: One-Click Google Colab Notebook (Recommended)

1. Click the **[Open in Colab](https://colab.research.google.com/github/chayne-wild/pdf-OCR-to-txt/blob/main/pdf_OCR_to_txt.ipynb)** badge at the top of this README.
2. Run **Step 1** once to install `poppler-utils`, `tesseract-ocr`, `pdf2image`, and `pytesseract`.
3. Run **Step 2** to upload one or more `.pdf` files from your computer. Once processing finishes, your browser will automatically download the resulting `<filename>_ocr_<timestamp>.txt` file(s).
4. Re-run **Step 2** as often as you like during your active session.

### Option 2: Manual Copy-Paste (Standalone `.py` Scripts)

If you prefer working in your own blank Colab notebook:

1. Copy the contents of [`00_install_dependencies.py`](00_install_dependencies.py) into your first Colab cell and run it once.
2. Copy the contents of [`01_upload_and_convert.py`](01_upload_and_convert.py) into a second cell and run it whenever you want to convert documents.

### Option 3: Clone Directly Inside a Colab Cell

```python
# Cell 1: Clone repository and install dependencies (Run Once)
!git clone [https://github.com/chayne-wild/pdf-OCR-to-txt.git](https://github.com/chayne-wild/pdf-OCR-to-txt.git)
%cd pdf-OCR-to-txt
%run 00_install_dependencies.py
```

```python
# Cell 2: Upload and convert PDFs (Re-run as needed)
%run 01_upload_and_convert.py
```

---

## Handling Complex Layouts & Non-Standard Formats

Standard OCR works best on clean, single-column pages. Documents with irregular formatting require special consideration or minor parameter adjustments in `01_upload_and_convert.py`:

### 1. Multi-Column Layouts, Sidebars, and Tables
While Tesseract's default mode (`--psm 3`) attempts to detect columns automatically, dense multi-column layouts (such as academic journals, newspapers, or two-column legal records), inset sidebars, and borderless tables can occasionally cause Tesseract to read straight across the horizontal axis—merging lines from adjacent columns.
* **Adjustment:** Pass the `config` argument to `pytesseract.image_to_string(image, config='...')` using one of Tesseract's Page Segmentation Modes (PSM):
  * `config='--psm 1'` : Automatic page segmentation with **Orientation and Script Detection (OSD)**. Often improves multi-column separation and handles accidentally rotated pages.
  * `config='--psm 4'` : Assumes a single column of text of variable sizes (useful when Tesseract falsely splits a single wide column or indented block quotes into multiple columns).
  * `config='--psm 6'` : Assumes a single uniform block of text (ideal for standard single-column book pages where headers/marginalia are minimal).
  * `config='--psm 11'` : Sparse text mode. Finds as much text as possible in no particular order (useful for diagrams, forms, or heavily fragmented layouts).

### 2. Marginalia, Running Headers, and Handwritten Notes
Handwritten annotations in the margins, line numbers, or degraded scan borders (black edges from photocopiers) are frequently misinterpreted by OCR engines as stray ASCII punctuation (`|`, `~`, `_`, `\`).
* **Adjustment:** Cropping scan borders prior to upload or applying basic image preprocessing (binarization/thresholding via `Pillow` or `OpenCV` before passing `image` to `pytesseract`) can significantly reduce noise.

### 3. Skewed Scans and Low-Resolution Originals
Tesseract accuracy drops sharply if a scanned page is tilted by more than a few degrees.
* **Resolution vs. Memory:** This tool rasterizes pages at `dpi=300`, the standard sweet spot for OCR accuracy. If you are processing very small print (e.g., 6pt footnotes), increasing `dpi=400` in `convert_from_path(filename, dpi=400)` can improve character recognition. Conversely, if you encounter Google Colab RAM limits on massive PDFs (200+ pages), lower the setting to `dpi=200` or split the PDF into smaller batches before uploading.

---

## Repository Structure

```text
pdf-OCR-to-txt/
├── .gitignore                 # Ignores temporary PDFs, OCR outputs, and Python cache
├── LICENSE                    # MIT License
├── README.md                  # Documentation
├── requirements.txt           # Python package dependencies
├── pdf_OCR_to_txt.ipynb       # One-click Google Colab interactive notebook
├── 00_install_dependencies.py # Standalone setup script (run once per session)
└── 01_upload_and_convert.py   # Standalone OCR conversion script (run repeatedly)
```

---

## Legal Disclaimer & Copyright Notice

This utility is provided strictly for educational, accessibility, archival, and legitimate research purposes (such as computational text analysis and personal accessibility accommodations). 

This tool should **not** be used to unlawfully reproduce, bypass digital rights management, or distribute copyright-protected works. Users are solely responsible for ensuring that their use of this software complies with applicable copyright laws and institutional policies. The author assumes no liability for misuse of this software. Use at your own risk.

---

## License

This project is released under the open **MIT License**. Feel free to use, modify, and distribute it as needed. See the [LICENSE](LICENSE) file for full details.
