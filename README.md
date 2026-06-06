# DomainSpecificRAGChatBot
Domain‑specific RAG chatbot for Raghu Engineering College using Flask, FAISS, and Gemini.

# Raghu Engineering College RAG Chatbot

A domain-specific AI chatbot that answers questions about **Raghu Engineering College** using official college documents (AQAR reports, regulations, etc.).  
It uses **Retrieval-Augmented Generation (RAG)** with LangChain, FAISS, Hugging Face embeddings, and Google's **Gemini** models to provide accurate, source-backed answers from your PDFs

---

## What this project does

- Lets students and staff ask questions in natural language such as:
  - "What are the attendance rules?"
  - "Tell me about the AQAR 2022–23 highlights."
- Loads college PDFs from the `docs/` folder, splits them into chunks, creates vector embeddings, and stores them in a **FAISS** vector store. 
- On each user query:
  1. Embeds the question and retrieves the top relevant chunks from FAISS.
  2. Sends those chunks + the question (and chat history) to **Gemini 2.5 Flash**.
  3. Returns a clear answer plus the source PDF file used for that answer. 

---

##  Tech stack

- **Backend:** Python, Flask
- **AI / RAG:**
  - LangChain community loaders & vectorstores
  - FAISS for vector search
  - `sentence-transformers/all-MiniLM-L6-v2` for text embeddings 
  - Google Gen AI (Gemini 2.5 Flash) for answer generation 
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Config:** `.env` for `GOOGLE_API_KEY`

---

## Project structure

```text
COLLEGE-RAG-CHATBOT/
├─ docs/                 # Input PDFs (AQAR, regulations, etc.)
│  ├─ 2022-23_AQAR.pdf
│  ├─ AR-23-ACADEMIC-R....pdf
│  └─ ...
├─ vectorstore/          # Saved FAISS index (auto-created)
│  ├─ index.faiss
│  └─ index.pkl
├─ templates/
│  └─ index.html         # Chat UI page
├─ static/
│  ├─ style.css          # Chat UI styles
│  └─ script.js          # Frontend chat logic
├─ create_vector_db.py   # Builds the FAISS vector store from PDFs
├─ app.py                # Flask app with RAG + Gemini + chat history
├─ .env                  # Contains GOOGLE_API_KEY (not committed)
├─ requirements.txt      # Python dependencies
└─ README.md
```

---

##  Setup and installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/college-rag-chatbot.git
cd college-rag-chatbot
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
venv/Scripts/activate   # On Windows
# source venv/bin/activate  # On macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Dependencies include Flask, LangChain community packages, FAISS, Hugging Face embeddings, python-dotenv, and the Google Gen AI SDK. 

### 4. Add your PDFs

- Put all your college documents (AQAR, regulations, etc.) into the `docs/` folder as `.pdf` files.

### 5. Configure API key

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

You can get a Gemini API key from Google AI Studio / Google Gen AI documentation. 

---

## 🧩 Step 1: Build the vector store

Run:

```bash
python create_vector_db.py
```

What this script does:

- Loads all PDFs from `docs/` using `PyPDFLoader`. 
- Splits them into chunks (~500 characters with overlap) using `RecursiveCharacterTextSplitter`. 
- Embeds each chunk with `sentence-transformers/all-MiniLM-L6-v2`. 
- Stores embeddings in a **FAISS** index and saves it into the `vectorstore/` folder. 

You should see messages like:

- `Loading: 2022-23_AQAR.pdf`
- `Loaded X pages`
- `Created Y chunks`
- `✅ Vector database created successfully!`

---

##  Step 2: Run the chatbot

Start the Flask server:

```bash
python app.py
```

- The app runs by default at `http://127.0.0.1:5000/` (or `http://localhost:5000/`).
- Open this URL in your browser.

---

##  How the web UI works

The frontend (in `templates/index.html`, `static/style.css`, `static/script.js`) provides a simple chat interface:

- **index.html**
  - Chat card with header (`Raghu College Assistant`), messages area, input box, and buttons.

- **style.css**
  - Modern chat design with:
    - Left‑aligned gray bot messages
    - Right‑aligned blue user messages
    - Typing indicator with animated dots
    - Clear chat button and responsive layout

- **script.js**
  - Sends the user’s question to `/chat` via POST (`fetch("/chat", {...})`).
  - Shows a “typing…” indicator while waiting for the response.
  - Displays the bot’s reply and a **Source: filename.pdf** tag.
  - Calls `/reset` when **Clear Chat** is clicked to reset conversation memory.

---

##  RAG + chat history flow

1. User types a question in the UI and clicks **Send**.
2. Frontend sends `{ "message": "..." }` to `/chat`.
3. Backend (Flask) does the following:
   - Adds the new question to an in‑memory `chat_history` list.
   - Uses FAISS `similarity_search` to retrieve the top 3 relevant chunks from the vector store.
   - Builds a prompt that includes:
     - Conversation history so far
     - Retrieved context from college documents
     - The current question
     - Instructions: “Answer ONLY using the provided context. If the answer is not in the context, say ‘I don’t have that information.’”
   - Sends this prompt to **Gemini 2.5 Flash** using the Google Gen AI Python SDK. 
   - Gets the model’s answer and appends it to `chat_history`.
   - Returns JSON: `{ reply: answer, source: first_source_file }`.

4. Frontend displays the answer and the source tag under the message.

5. `/reset` endpoint clears `chat_history` so the next conversation starts fresh.

---

## ✅ Features

- Uses **official college PDFs** as the only knowledge base.
- **Reduces hallucinations** by forcing the model to answer only from retrieved context.
- Shows **source file name** for every answer.
- Maintains **chat history** to support follow‑up questions.
- Clean, responsive **chat UI** built with HTML/CSS/JS.
- Easy to extend with more documents—just add PDFs and rebuild the vector store.

---

##  Possible improvements

- Show multiple source files instead of only the first one.
- Highlight the exact paragraph used in the answer.
- Add authentication (e.g., only for college students/staff).
- Deploy to a cloud platform (Render, Railway, or any VPS) and secure the `.env` file.

---

##  Author

- Name: THADELA NIHARIKA  
- Location:Visakhapatnam,AndhraPradesh, India  
- GitHub: `(https://github.com/Niha-868)` (update this)

---

##  License

This project is for educational and internal use.  
You can choose a license such as **MIT** or **Apache-2.0** and update this section.
