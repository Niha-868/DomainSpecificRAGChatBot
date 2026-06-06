from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

query = "What is the minimum attendance requirement?"

results = db.similarity_search(query, k=3)

for i, doc in enumerate(results):
    print(f"\nResult {i+1}")
    print(doc.page_content[:500])