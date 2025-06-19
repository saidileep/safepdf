"""SafePDF – Streamlit Cloud entrypoint.

This file is identical to `safe_pdf.py` in the project root but placed
here so Streamlit Cloud can automatically run `streamlit run streamlit_app.py`.
"""
# === BEGIN COPIED APP CODE ===
from __future__ import annotations

import tempfile
import os
from pathlib import Path
from typing import Optional

import streamlit as st

# Import the unlock helper from the same directory
import importlib

unlock_pdf_spec = importlib.util.spec_from_file_location(
    "unlock_pdf", str(Path(__file__).parent / "unlock_pdf.py")
)
unlock_pdf_module = importlib.util.module_from_spec(unlock_pdf_spec)  # type: ignore
if unlock_pdf_spec and unlock_pdf_spec.loader:
    unlock_pdf_spec.loader.exec_module(unlock_pdf_module)  # type: ignore

unlock_pdf_func = unlock_pdf_module.unlock_pdf  # type: ignore

st.set_page_config(
    page_title="SafePDF – Unlock Your PDFs",
    page_icon="🔓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------   Custom Styles   ------------------------ #
CUSTOM_CSS = """
<style>
/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {
  --accent: #7a5cff;
  --accent-light: #a78bff;
  --card-radius: 20px;
  --shadow: 0 10px 30px rgba(0,0,0,0.08);
}

/* ----------  Base  ---------- */
html, body, [class*="st-"] {
  font-family: 'Poppins', sans-serif;
  color: #343a40;
  font-weight: 400;
}

.stApp {
  /* Multi-color diagonal gradient */
  background: linear-gradient(130deg,#ece9ff 0%, #e1f0ff 35%, #e7fff5 70%, #fffae7 100%);
}

/* Hide Streamlit default chrome */
header, footer {visibility: hidden;}

/* Narrow container */
.block-container {
  max-width: 480px;
  padding-top: 4rem;
}

/* ----------  Card  ---------- */
.card {
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow);
  padding: 2.5rem 2rem;
}

/* ----------  Components  ---------- */
.stTextInput, .stButton {
  width: 100%;
}

/* Text input */
.stTextInput input {
  border: 1px solid #d0d0d0;
  border-radius: 12px;
  padding: 0.7rem 0.9rem;
}

/* Primary button */
.stButton>button {
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 14px;
  font-weight: 600;
  padding: 0.75rem 0;
  width: 100%;
  transition: background .2s ease, transform .1s ease;
}
.stButton>button:hover {
  background: var(--accent-light);
}
.stButton>button:active {
  transform: translateY(1px);
}

/* Success & error boxes */
.stAlert {
  border-radius: 12px;
  font-size: 0.9rem;
}

/* Heading */
h1 {
  font-weight: 700;
  text-align: center;
  margin-bottom: 0.25em;
}

p.tagline {
  text-align: center;
  color: #555;
  margin-top: 0;
  font-size: 0.95rem;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ------------------------   App UI   ------------------------ #

st.markdown(
    """<div class='center'>
    <h1 style='margin-bottom:0.2em;'>🔒 SafePDF</h1>
    <p style='color:#4a4a4a;margin-top:0;'>Effortlessly unlock your password-protected PDFs.</p>
</div>""",
    unsafe_allow_html=True,
)

# Upload Section (simple uploader)
uploaded_file = st.file_uploader(
    "Select a locked PDF", type=["pdf"], accept_multiple_files=False
)

password: Optional[str] = None
if uploaded_file is not None:
    password = st.text_input("Enter PDF password", type="password", placeholder="●●●●●●")

if uploaded_file is not None and password:
    if st.button("Unlock PDF", type="primary"):
        with st.spinner("Unlocking…"):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    tmp_in_path = tmp_in.name

                output_path = unlock_pdf_func(tmp_in_path, password)

                with open(output_path, "rb") as f_out:
                    unlocked_bytes = f_out.read()

                out_filename = Path(uploaded_file.name).stem + "_unlocked.pdf"

                st.success("PDF unlocked successfully!")
                st.download_button(
                    label="📥 Download Unlocked PDF",
                    data=unlocked_bytes,
                    file_name=out_filename,
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                try:
                    os.remove(tmp_in_path)
                    os.remove(output_path)
                except Exception:
                    pass
# === END APP CODE === 