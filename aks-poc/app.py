import os
import requests
from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

# ----------------------------
# Azure OpenAI configuration
# ----------------------------
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-chat")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# ----------------------------
# RAG document configuration
# ----------------------------
DOC_PATH = Path(os.getenv("RAG_DOC_PATH", "docs/source.txt"))

# ----------------------------
# Health check
# ----------------------------
@app.get("/health")
def health():
    return jsonify({"status": "ok"})


# ----------------------------
# Simple chat endpoint
# ----------------------------
@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "Send JSON: {\"text\":\"...\"}"}), 400

    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions"
    params = {"api-version": AZURE_OPENAI_API_VERSION}
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }

    payload = {
        "messages": [
            {"role": "user", "content": text}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
    }

    r = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
    r.raise_for_status()

    j = r.json()
    answer = j["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})


# ----------------------------
# RAG v1 endpoint
# ----------------------------
@app.post("/rag")
def rag():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"error": "Send JSON: {\"question\":\"...\"}"}), 400

    if not DOC_PATH.exists():
        return jsonify({"error": f"Document not found: {DOC_PATH}"}), 500

    document_text = DOC_PATH.read_text(encoding="utf-8")

    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions"
    params = {"api-version": AZURE_OPENAI_API_VERSION}
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Answer ONLY using the DOCUMENT below. "
                    "If the answer is not contained in the document, say: "
                    "'I do not know based on the provided document.'"
                ),
            },
            {
                "role": "user",
                "content": f"DOCUMENT:\n{document_text}\n\nQUESTION:\n{question}",
            },
        ],
        "max_tokens": 200,
        "temperature": 0.2,
    }

    r = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
    r.raise_for_status()

    j = r.json()
    answer = j["choices"][0]["message"]["content"]

    return jsonify({
        "answer": answer,
        "source": str(DOC_PATH)
    })


# ----------------------------
# App entrypoint
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)