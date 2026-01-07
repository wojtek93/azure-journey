import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-chat")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-07-01-preview")

@app.get("/health")
def health():
    return "ok", 200

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_text = data.get("text", "").strip()
    if not user_text:
        return jsonify({"error": "Send JSON: {\"text\":\"...\"}"}), 400

    url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT}/chat/completions"
    params = {"api-version": AZURE_OPENAI_API_VERSION}
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text},
        ],
        "max_tokens": 120,
        "temperature": 0.7,
    }

    r = requests.post(url, params=params, headers=headers, json=payload, timeout=30)
    if r.status_code >= 400:
        return jsonify({"status": r.status_code, "body": r.text}), 500

    j = r.json()
    answer = j["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})
