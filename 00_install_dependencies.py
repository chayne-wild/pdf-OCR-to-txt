# 00_install_dependencies.py
# Run ONCE per Google Colab session to install system binaries and Python libraries.
# Compatible with direct copy-pasting into a Colab cell or running via %run.

import subprocess
import sys

def install_dependencies():
    print("Step 1/3: Updating apt package lists...")
    subprocess.run(["apt-get", "update", "-qq"], check=True)
    
    print("Step 2/3: Installing system binaries (poppler-utils, tesseract-ocr)...")
    subprocess.run(
        ["apt-get", "install", "-y", "-qq", "poppler-utils", "tesseract-ocr"],
        check=True
    )
    
    print("Step 3/3: Installing Python libraries (pdf2image, pytesseract)...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "pdf2image", "pytesseract"],
        check=True
    )
    
    print("\nSetup complete! Dependencies are installed for this session.")
    print("You can now run 01_upload_and_convert.py as many times as needed without re-running this script.")

if __name__ == "__main__":
    install_dependencies()
