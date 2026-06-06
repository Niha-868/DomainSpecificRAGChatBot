const messagesDiv = document.getElementById("chatMessages");
const userInput   = document.getElementById("userInput");
const sendBtn     = document.getElementById("sendBtn");
const clearBtn    = document.getElementById("clearBtn");

// ── helpers ──────────────────────────────────────────────

function scrollToBottom() {
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function appendMessage(role, text, source = null) {
  const wrapper = document.createElement("div");

  const bubble = document.createElement("div");
  bubble.classList.add("message", role === "user" ? "user-message" : "bot-message");
  bubble.textContent = text;
  wrapper.appendChild(bubble);

  if (source && role === "bot") {
    const tag = document.createElement("p");
    tag.classList.add("source-tag");
    // show only the filename, not the full path
    const filename = source.split("/").pop().split("\\").pop();
    tag.textContent = "Source: " + filename;
    wrapper.appendChild(tag);
  }

  messagesDiv.appendChild(wrapper);
  scrollToBottom();
}

function showTyping() {
  const el = document.createElement("div");
  el.classList.add("typing-indicator");
  el.id = "typingIndicator";
  el.innerHTML = "<span></span><span></span><span></span>";
  messagesDiv.appendChild(el);
  scrollToBottom();
  return el;
}

function removeTyping() {
  const el = document.getElementById("typingIndicator");
  if (el) el.remove();
}

// ── send message ─────────────────────────────────────────

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage("user", text);
  userInput.value = "";
  sendBtn.disabled = true;

  const typing = showTyping();

  try {
    const res  = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    removeTyping();
    appendMessage("bot", data.reply, data.source);
  } catch (err) {
    removeTyping();
    appendMessage("bot", "Something went wrong. Please try again.");
  }

  sendBtn.disabled = false;
  userInput.focus();
}

// ── clear chat ────────────────────────────────────────────

async function clearChat() {
  try {
    await fetch("/reset", { method: "POST" });
  } catch (err) {
    console.warn("Reset endpoint error:", err);
  }

  // clear UI — keep only the welcome message
  messagesDiv.innerHTML = `
    <div class="message bot-message">
      <p>Hello! I'm your Raghu Engineering College assistant. Ask me anything about fees, academics, rules, or college documents.</p>
    </div>`;
}

// ── event listeners ───────────────────────────────────────

sendBtn.addEventListener("click", sendMessage);
clearBtn.addEventListener("click", clearChat);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});