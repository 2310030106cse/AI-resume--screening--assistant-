import os
import sys
import time
import tempfile

import streamlit as st

# Make src/ importable from frontend/ (rag.py uses flat imports like
# "from pdf_loader import ...", so src/ itself must be on the path)
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from rag import build_vector_store_from_file, screen_resume
from pdf_loader import extract_text_from_file

st.set_page_config(page_title="AI Resume Screening Assistant", page_icon="📄", layout="centered")

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def reset_state():
    st.session_state.result = None
    st.session_state.error = None


if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

st.title("📄 AI Resume Screening Assistant")
st.write("Upload a resume (PDF, Word, or TXT) and paste a job description to get an AI-powered match analysis.")

uploaded_file = st.file_uploader("Upload Resume", type=list(ALLOWED_EXTENSIONS))
job_description = st.text_area("Job Description", height=200, placeholder="Paste the job description here...")

col1, col2 = st.columns([1, 1])
screen_clicked = col1.button("Screen Resume", type="primary", use_container_width=True)
clear_clicked = col2.button("Clear", use_container_width=True)

if clear_clicked:
    reset_state()
    st.rerun()

if screen_clicked:
    reset_state()

    # --- Validation ---
    if not uploaded_file:
        st.session_state.error = "❌ Please upload a resume."
    elif not job_description.strip():
        st.session_state.error = "❌ Please enter a job description."
    else:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower().lstrip(".")
        if file_ext not in ALLOWED_EXTENSIONS:
            st.session_state.error = "❌ Unsupported file type. Please upload a PDF, DOCX, or TXT file."

    if not st.session_state.error:
        progress_text = st.empty()
        progress_bar = st.progress(0)

        try:
            # Step 1: Save uploaded file
            progress_text.write("📤 Uploading Resume...")
            progress_bar.progress(25)
            file_ext_with_dot = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext_with_dot) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            time.sleep(0.3)

            # Step 2: Extract text
            progress_text.write("📝 Extracting Text...")
            progress_bar.progress(50)
            extracted_text = extract_text_from_file(tmp_path)

            if not extracted_text.strip():
                os.remove(tmp_path)
                progress_bar.empty()
                progress_text.empty()
                st.session_state.error = (
                    "❌ No text could be extracted from this file. "
                    "If it's a PDF, it may be a scanned image rather than text-based. "
                    "Try a resume exported from Word/Google Docs instead."
                )
            else:
                # Step 3: Analyze
                progress_text.write("🔎 Analyzing Resume...")
                progress_bar.progress(75)
                with st.spinner("🔄 Analyzing Resume..."):
                    vector_store = build_vector_store_from_file(tmp_path)
                    result = screen_resume(vector_store, job_description)

                os.remove(tmp_path)

                # Step 4: Done
                progress_text.write("✅ Generating Result...")
                progress_bar.progress(100)
                time.sleep(0.3)
                progress_bar.empty()
                progress_text.empty()

                st.session_state.result = result

        except Exception as e:
            progress_bar.empty()
            progress_text.empty()
            st.session_state.error = f"❌ Something went wrong: {e}"

# --- Display error ---
if st.session_state.error:
    st.error(st.session_state.error)

# --- Display result ---
if st.session_state.result:
    result = st.session_state.result

    st.success("✅ Resume analyzed successfully!")

    if result.get("candidate_summary"):
        st.markdown("### 🧑‍💼 Candidate Summary")
        st.write(result["candidate_summary"])

    if result.get("experience_level") and result["experience_level"] not in (None, "Unknown"):
        st.markdown(f"**Experience Level:** {result['experience_level']}")

    if result.get("match_score") is not None:
        score_col, ats_col = st.columns(2)
        with score_col:
            st.markdown("### 🎯 Match Score")
            st.markdown(f"## {result['match_score']}%")
            st.progress(min(max(result["match_score"], 0), 100) / 100)
        with ats_col:
            if result.get("ats_score") is not None:
                st.markdown("### 📋 ATS Score")
                st.markdown(f"## {result['ats_score']}%")
                st.progress(min(max(result["ats_score"], 0), 100) / 100)
    else:
        # Fallback: model didn't return valid JSON, show raw recommendation text
        st.markdown("### Result")
        st.markdown(result.get("recommendation", "No result available."))

    if result.get("hiring_decision") and result["hiring_decision"] not in (None, "Unknown"):
        decision = result["hiring_decision"]
        decision_colors = {
            "Strong Match": "🟢",
            "Consider": "🟡",
            "Weak Match": "🟠",
            "Not a Fit": "🔴",
        }
        icon = decision_colors.get(decision, "⚪")
        st.markdown(f"### {icon} Hiring Decision: {decision}")

    if result.get("top_skills"):
        st.markdown("---")
        st.markdown("### ⭐ Top Skills")
        for skill in result["top_skills"]:
            st.markdown(f"- {skill}")

    if result.get("matching_skills"):
        st.markdown("---")
        st.markdown("### ✅ Matching Skills")
        for skill in result["matching_skills"]:
            st.markdown(f"- {skill}")

    if result.get("missing_skills"):
        st.markdown("---")
        st.markdown("### ❌ Missing Skills")
        for skill in result["missing_skills"]:
            st.markdown(f"- {skill}")

    if result.get("interview_questions"):
        st.markdown("---")
        st.markdown("### ❓ Recommended Interview Questions")
        for i, question in enumerate(result["interview_questions"], start=1):
            st.markdown(f"{i}. {question}")

    if result.get("match_score") is not None and result.get("recommendation"):
        st.markdown("---")
        st.markdown("### 💡 Recommendation")
        st.info(result["recommendation"])