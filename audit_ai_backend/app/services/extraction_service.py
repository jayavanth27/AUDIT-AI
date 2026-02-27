"""Document extraction utilities: convert uploads to text and structured fields."""

from typing import BinaryIO, Dict, Any

import pdfplumber
import fitz  # PyMuPDF
import docx
import pandas as pd


def extract_from_pdf(file: BinaryIO) -> str:
    """Return plain text extracted from a PDF binary stream.

    Attempts `pdfplumber` first, falls back to PyMuPDF on failure.
    """
    text = []
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text.append(page.extract_text() or "")
    except Exception:
        # fallback to PyMuPDF
        file.seek(0)
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)


def extract_from_docx(file: BinaryIO) -> str:
    """Extract text from a DOCX file object."""
    doc = docx.Document(file)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_from_csv(file: BinaryIO) -> str:
    """Read a CSV file into a canonical CSV string for downstream parsing."""
    file.seek(0)
    df = pd.read_csv(file)
    return df.to_csv(index=False)


def parse_structured(text: str) -> Dict[str, Any]:
    """Perform lightweight regex-based field extraction from text.

    Looks for invoice number, amount, and ISO dates.
    """
    fields: Dict[str, Any] = {}
    lines = text.splitlines()
    for line in lines:
        if "invoice" in line.lower() and "number" in line.lower():
            parts = line.split()
            for part in parts:
                if part.isdigit():
                    fields["invoice_number"] = part
        if any(k in line.lower() for k in ["amount", "total"]):
            # find numbers
            import re

            match = re.search(r"\d+[\.,]?\d*", line.replace(",", ""))
            if match:
                fields["amount"] = float(match.group())
        if any(k in line.lower() for k in ["date", "due"]):
            # naive date detection
            import re

            match = re.search(r"\d{4}-\d{2}-\d{2}", line)
            if match:
                fields["date"] = match.group()
    return fields


def extract_document(file: BinaryIO, filename: str, content_type: str) -> Dict[str, Any]:
    """Main entry for extraction that dispatches based on content type."""
    file.seek(0)
    lower = filename.lower()
    text = ""
    if lower.endswith(".pdf") or content_type == "application/pdf":
        text = extract_from_pdf(file)
    elif lower.endswith(".docx"):
        text = extract_from_docx(file)
    elif lower.endswith(".csv") or "csv" in content_type:
        text = extract_from_csv(file)
    else:
        # try to read as text
        try:
            text = file.read().decode("utf-8", errors="ignore")
        except Exception:
            text = ""
    structured = parse_structured(text)
    return {"document_type": None, "fields": structured, "raw_text": text}
