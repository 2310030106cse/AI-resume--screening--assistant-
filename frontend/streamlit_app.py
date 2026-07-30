import os
import sys
import tempfile

import streamlit as st

# Make src/ importable from frontend/ (rag.py uses flat imports like
# "from pdf_loader import ...", so src/ itself must be on the path)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from rag import build_vector_store_from_file, screen_resume
from pdf_loader import extract_text_from_file

st.set_page_config(page_title="AI Resume Screening Assistant", page_icon="📄")

st.title("📄 AI Resume Screening Assistant")
st.write("Upload a resume (PDF, Word, or TXT) and paste a job description to get an AI-powered match analysis.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")

if st.button("Screen Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload a resume file first.")
    elif not job_description.strip():
        st.error("Please paste a job description first.")
    else:
        with st.spinner("Reading resume and analyzing against job description..."):
            try:
                # Save uploaded file to a temp path with its original extension
                file_ext = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                extracted_text = extract_text_from_file(tmp_path)

                if not extracted_text.strip():
                    os.remove(tmp_path)
                    st.error(
                        "No text could be extracted from this file. "
                        "If it's a PDF, it may be a scanned image rather than text-based. "
                        "Try a resume exported from Word/Google Docs instead."
                    )
                else:
                    vector_store = build_vector_store_from_file(tmp_path)
                    result = screen_resume(vector_store, job_description)

                    os.remove(tmp_path)

                    st.success("Screening complete!")
                    st.markdown(result)

            except Exception as e:
                st.error(f"Something went wrong: {e}")