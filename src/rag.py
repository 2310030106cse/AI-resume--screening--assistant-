import os
from dotenv import load_dotenv
from groq import Groq

from pdf_loader import extract_text_from_file
from text_splitter import split_text
from embeddings import get_embedding_model
from vector_store import create_vector_store
from prompts import build_screening_prompt

load_dotenv()

GROQ_MODEL = "llama-3.3-70b-versatile"


def get_groq_client():
    """
    Creates and returns a Groq client using the API key from .env.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env")

    return Groq(api_key=api_key)


def build_vector_store_from_file(file_path):
    """
    Full pipeline: resume file (.pdf/.docx/.txt) -> raw text -> chunks
    -> embeddings -> FAISS vector store.
    """
    raw_text = extract_text_from_file(file_path)
    chunks = split_text(raw_text)
    embedding_model = get_embedding_model()
    vector_store = create_vector_store(chunks, embedding_model)

    return vector_store


def retrieve_relevant_chunks(vector_store, job_description, top_k=4):
    """
    Retrieves the top_k resume chunks most relevant to the job description.
    """
    results = vector_store.similarity_search(job_description, k=top_k)
    return [doc.page_content for doc in results]


def screen_resume(vector_store, job_description, top_k=4):
    """
    Retrieves relevant resume chunks and asks Groq's LLM to screen the
    candidate against the given job description. Returns the model's
    screening summary as a string.
    """
    relevant_chunks = retrieve_relevant_chunks(vector_store, job_description, top_k=top_k)
    context = "\n\n---\n\n".join(relevant_chunks)

    prompt = build_screening_prompt(context=context, job_description=job_description)

    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Quick manual test
    file_path = "data/sample_resume.pdf"
    job_description = "Looking for a Python developer with experience in machine learning and REST APIs."

    vs = build_vector_store_from_file(file_path)
    result = screen_resume(vs, job_description)

    print(result)