from src.pdf_loader import extract_text_from_pdf
from src.text_splitter import split_text
from src.embeddings import get_embedding_model
from src.vector_store import create_vector_store

# Step 1: Load Resume
pdf_path = "data/sample_resume.pdf"

# Step 2: Extract Text
text = extract_text_from_pdf(pdf_path)

# Step 3: Split into Chunks
chunks = split_text(text)

print(f"Total Chunks: {len(chunks)}")

# Step 4: Load Embedding Model
embedding_model = get_embedding_model()

# Step 5: Create Vector Database
vector_store = create_vector_store(chunks, embedding_model)

print("\n✅ FAISS Vector Database Created Successfully!")

print(f"\nTotal Documents Stored: {vector_store.index.ntotal}")

print("\n" + "=" * 60)
print("Testing Semantic Search")
print("=" * 60)

query = "What programming languages does the candidate know?"

results = vector_store.similarity_search(query, k=2)

for i, doc in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("-" * 50)
    print(doc.page_content)