# AI Resume Screening Assistant

An AI-powered Resume Screening Assistant that uses Retrieval-Augmented Generation (RAG) to analyze resumes, extract relevant information, and answer recruiter questions intelligently.

## Features

- Upload PDF resumes
- Extract text from resumes
- Split text into chunks
- Generate embeddings
- Store embeddings using FAISS
- Semantic search
- AI-powered question answering using Gemini

## Tech Stack

- Python
- FastAPI
- LangChain
- FAISS
- Streamlit
- Google Gemini API
- Hugging Face Embeddings

## Project Structure

```
AI-Resume-Screening-Assistant/
│
├── api/
├── data/
├── frontend/
├── src/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

```bash
git clone <repository-url>

cd AI-Resume-Screening-Assistant

pip install -r requirements.txt

streamlit run frontend/streamlit_app.py
```

## Future Improvements

- Multiple resume support
- Skill matching
- ATS score prediction
- Resume ranking
- Interview question generation

## Author

Kurakula Vaishnavi Devi