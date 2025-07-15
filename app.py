# app.py
import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 1. Configuration from env vars (with sensible defaults)
API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
API_KEY  = os.getenv("OPENAI_API_KEY", "dummy-key")
MODEL    = "colossal-llama-2-7b-base"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify(reply="(no prompt)"), 400

    # 2. Build the payload exactly as LM Studio expects at /v1/completions
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 3. POST to the local LM Studio endpoint
    resp = requests.post(f"{API_BASE}/completions", json=payload, headers=headers)
    if not resp.ok:
        # surface any server-side error
        return jsonify(error=f"{resp.status_code} {resp.text}"), 500

    # 4. Parse out the generated text
    body = resp.json()
    text = body.get("choices", [{}])[0].get("text", "").strip()
    return jsonify(reply=text)

if __name__ == '__main__':
    app.run()
