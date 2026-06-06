import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# Load all PDFs
documents = []

for file in os.listdir("docs"):
    if file.endswith(".pdf"):
        path = os.path.join("docs", file)

        print(f"Loading: {file}")

        loader = PyPDFLoader(path)
        documents.extend(loader.load())

print(f"Loaded {len(documents)} pages")

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

print(f"Created {len(docs)} chunks")

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector DB
db = FAISS.from_documents(
    docs,
    embeddings
)

# Save
db.save_local("vectorstore")

print("✅ Vector database created successfully!")