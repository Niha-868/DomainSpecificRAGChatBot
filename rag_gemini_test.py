from dotenv import load_dotenv
from google import genai
import os

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

question = input("Ask a question: ")

docs = db.similarity_search(question, k=3)

source_file = docs[0].metadata.get("source", "Unknown")

context = "\n\n".join(
    [doc.page_content for doc in docs]
)

prompt = f"""
You are a helpful college assistant.

Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print("\nAnswer:")
print(response.text)