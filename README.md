#  College RAG Chatbot

> A domain-specific AI chatbot that answers questions from college documents using **Retrieval-Augmented Generation (RAG)** — powered by Google Gemini, LangChain, FAISS, and Flask.

---

##  Problem It Solves

Students and staff often struggle to find specific information buried inside large college PDF documents — handbooks, academic reports, maintenance records, AQAR reports, and more. Manually searching through hundreds of pages is time-consuming and frustrating.

This chatbot solves that by letting users **ask natural language questions** and get **instant, accurate answers grounded in the actual college documents** — with the source PDF cited for every answer. Users can also **upload their own PDFs** and chat with any document on the fly.

---

##  How It Works (RAG Pipeline)

```
PDF Documents → Chunking → Embeddings → FAISS Vector Store
                                                  ↓
User Question → Embed Question → Similarity Search → Top 3 Chunks
                                                          ↓
                                         Gemini 2.5 Flash → Answer + Source
```

1. Indexing — PDFs are loaded, split into 500-character chunks, embedded using `all-MiniLM-L6-v2`, and stored in a FAISS vector index.
2. Retrieval — When a user asks a question, the top 3 most semantically similar chunks are retrieved from FAISS.
3. Generation — The retrieved chunks + conversation history are passed to Gemini 2.5 Flash, which generates a grounded answer.

---

##  Tech Stack

| Layer |                     | Technology |

| LLM|                   | Google Gemini 2.5 Flash (`google-genai`) |
| Embeddings |           |`sentence-transformers/all-MiniLM-L6-v2` via `langchain-huggingface` |
| Vector Store|          |FAISS (Facebook AI Similarity Search) |
| Orchestration|         |LangChain |
| Backend|               | Python + Flask |
| Frontend |             | HTML, CSS, JavaScript (vanilla) |
| PDF Parsing |          | PyPDFLoader (LangChain) |
| Environment |          |python-dotenv |

---

##  Project Structure

```
collegeRAGassistent/
│
├── docs/                        # College PDF documents (knowledge base)
│   ├── 2022-23_AQAR.pdf
│   ├── AR-23-ACADEMIC-R.pdf
│   └── raghuclgmaintanen.pdf
│
├── vectorstore/                 # Auto-generated FAISS index (do not edit)
│   ├── index.faiss
│   └── index.pkl
│
├── static/
│   ├── style.css                # Chat UI styles
│   └── script.js                # Frontend logic
│
├── templates/
│   └── index.html               # Chat interface
│
├── app.py                       # Flask server + RAG pipeline
├── create_vector_db.py          # One-time script to build FAISS index
├── rag_gemini_test.py           # Test script for Gemini + RAG
├── test_rag.py                  # Test script for retrieval
├── requirements.txt             # Python dependencies
└── .env                         # API keys (not committed to Git)
```

---

##  Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/collegeRAGassistent.git
cd collegeRAGassistent
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Google Gemini API key

Create a `.env` file in the root folder:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get your free API key at [https://aistudio.google.com](https://aistudio.google.com)

### 5. Add your PDF documents

Place your PDF files inside the `docs/` folder.

### 6. Build the vector database (run once)

```bash
python create_vector_db.py
```

This reads all PDFs in `docs/`, creates embeddings, and saves the FAISS index to `vectorstore/`.

### 7. Run the chatbot

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

---

##  Features

- Natural language Q&A over college PDF documents
- Upload your own PDF and chat with any document instantly
- Chat history memory — supports follow-up questions in context
- Source citation — every answer shows which PDF it came from
- Switch modes — toggle between college docs and your uploaded PDF
- Clear chat — reset conversation history with one click
- Responsive UI — works on mobile and desktop

---

##  requirements.txt

```
flask
python-dotenv
google-genai
langchain
langchain-huggingface
langchain-community
faiss-cpu
sentence-transformers
pypdf
```

---

##  Environment Variables

| Variable | Description |

| `GOOGLE_API_KEY`  --> Your Google Gemini API key from AI Studio |

> ⚠️ Never commit your `.env` file to GitHub. Add it to `.gitignore`.

---

##  Example Questions to Ask

**Basic factual questions**

What is the vision and mission of Raghu Engineering College?
What are the departments available in the college?
What is the NAAC accreditation status of the college?

**Academic questions**

What are the rules for attendance?
What is the minimum CGPA required to pass?
How many credits are required to complete the degree?

**Testing RAG retrieval**

What activities were conducted under the IQAC?
What are the research publications mentioned in the report?
How many students were placed in the academic year 2022-23?

**Testing chat memory (ask these one after another)**

How many students are enrolled in CSE?
What percentage of them got placed?
Which companies recruited the most from that branch?

---

##  Future Improvements

-  Deploy on Render / Railway (free cloud hosting)
-  Add support for multiple simultaneous PDFs
-  Add thumbs up / down feedback on answers
-  Persistent chat history using SQLite
-  Multi-language support

---

##  Author

**Niharika**
B.Tech CSE (AI & ML) — Raghu Engineering College, Visakhapatnam

<img width="483" height="524" alt="image" src="https://github.com/user-attachments/assets/888aa501-44fe-421f-b040-10edac4fef0e" />


---

##  License

This project is open source and available under the [MIT License](LICENSE).
