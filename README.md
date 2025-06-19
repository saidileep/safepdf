# SafePDF – Unlock password-protected PDFs in your browser

SafePDF is a Streamlit web app that lets you upload a locked PDF, enter its password, and instantly download an un-encrypted copy.

## 🗂 Project structure

```
safe_pdf_app/
├── streamlit_app.py   # Main Streamlit UI (auto-run on Streamlit Cloud)
├── unlock_pdf.py      # PDF-unlocking helper
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## 🚀 Deploy on Streamlit Community Cloud

1. Push the `safe_pdf_app` folder to a public GitHub repository **or** create a new repo containing only these files.
2. Sign in to [streamlit.io/cloud](https://streamlit.io/cloud) and click **"New app"**.
3. Select your repository and branch, and set **`streamlit_app.py`** as the main file (default value).
4. Click **"Deploy"** – Streamlit Cloud will install the packages in `requirements.txt` and launch your app.

That's it! Share the generated URL with anyone who needs to unlock PDFs securely.

---
**Local development**

```bash
# clone repo and cd into it
python -m venv venv && source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501` by default. 