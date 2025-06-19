#!/usr/bin/env python3
"""unlock_pdf.py – utility module used by `streamlit_app.py`."""
# === BEGIN COPIED CODE ===
import argparse
import os
import sys

try:
    from pypdf import PdfReader, PdfWriter  # type: ignore
except ImportError:
    try:
        from PyPDF2 import PdfReader, PdfWriter  # type: ignore
    except ImportError:  # pragma: no cover
        sys.stderr.write(
            "PyPDF2 (or pypdf) is required. Install with `pip install pypdf`\n"
        )
        sys.exit(1)


def _output_path(input_path: str) -> str:
    directory, filename = os.path.split(input_path)
    basename, ext = os.path.splitext(filename)
    return os.path.join(directory, f"{basename}_unlocked{ext}")


def unlock_pdf(input_path: str, password: str) -> str:
    reader = PdfReader(input_path)

    if reader.is_encrypted:
        if reader.decrypt(password) == 0:
            raise ValueError("Failed to decrypt PDF. Check the password.")
    else:
        sys.stderr.write("Warning: PDF is not encrypted. Copying pages anyway.\n")

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    output_path = _output_path(input_path)
    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unlock a password-protected PDF.")
    parser.add_argument("pdf_path", help="Path to the locked PDF")
    parser.add_argument("password", help="Password for the PDF")
    args = parser.parse_args()
    print(unlock_pdf(args.pdf_path, args.password))
# === END COPIED CODE === 