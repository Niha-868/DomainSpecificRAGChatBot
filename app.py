from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

app = Flask(__name__)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history          # ✅ FIXES the UnboundLocalError

    user_question = request.json.get("message")
    chat_history.append({"role": "user", "content": user_question})

    docs = db.similarity_search(user_question, k=3)
    context = "\n\n".join([doc.page_content for doc in docs])

    history_text = ""
    for turn in chat_history[:-1]:
        role = "User" if turn["role"] == "user" else "Assistant"
        history_text += f"{role}: {turn['content']}\n"

    prompt = f"""
You are a college assistant chatbot for Raghu Engineering College.
Answer ONLY using the provided context.
If the answer is not in the context, say "I don't have that information."

Conversation so far:
{history_text}

Relevant context from college documents:
{context}

Current question: {user_question}
Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    answer = response.text

    chat_history.append({"role": "assistant", "content": answer})

    if len(chat_history) > 10:
        chat_history = chat_history[-10:]

    source_file = docs[0].metadata.get("source", "Unknown")
    return jsonify({"reply": answer, "source": source_file})


@app.route("/reset", methods=["POST"])
def reset():
    global chat_history          # ✅ already correct
    chat_history = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)