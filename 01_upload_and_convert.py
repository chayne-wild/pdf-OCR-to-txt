# 01_upload_and_convert.py
# Convert uploaded PDF document(s) to plain text (.txt) via 300 DPI OCR.
# Once 00_install_dependencies.py has been run in your current Colab session,
# you can run this script repeatedly without reinstalling dependencies.

import os
from datetime import datetime
from google.colab import files
from pdf2image import convert_from_path
import pytesseract

def process_pdf_to_txt():
    print("Please select your PDF file(s) to upload:")
    uploaded = files.upload()

    if not uploaded:
        print("No file uploaded. Execution stopped.")
        return

    for filename in uploaded.keys():
        if not filename.lower().endswith('.pdf'):
            print(f"Skipping '{filename}': Not a PDF file.")
            continue

        print(f"\nConverting '{filename}' to high-resolution images (300 DPI)...")
        # 300 DPI is standard for high-accuracy OCR
        images = convert_from_path(filename, dpi=300)

        full_text = []
        total_pages = len(images)

        for i, image in enumerate(images):
            print(f"Running OCR on page {i + 1} of {total_pages}...")
            # Using default Tesseract configuration (--psm 3: fully automatic page segmentation).
            # For uniform single-column pages, you can pass: config='--psm 6'
            # For complex multi-column pages with orientation detection, pass: config='--psm 1'
            page_text = pytesseract.image_to_string(image)
            full_text.append(page_text)

        # Join pages with a clear delimiter
        final_text = "\n\n--- Page Break ---\n\n".join(full_text)

        # Generate collision-proof filename using base name + timestamp
        base_name = os.path.splitext(filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{base_name}_ocr_{timestamp}.txt"

        with open(output_filename, "w", encoding="utf-8") as text_file:
            text_file.write(final_text)

        print(f"OCR complete for '{filename}'. Triggering download for '{output_filename}'...")
        files.download(output_filename)

if __name__ == "__main__":
    process_pdf_to_txt()
