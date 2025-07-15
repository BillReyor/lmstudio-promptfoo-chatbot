# app.py
import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration from environment variables (with sensible defaults)
API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
API_KEY  = os.getenv("OPENAI_API_KEY", "dummy-key")
MODEL    = "colossal-llama-2-7b-base"

# System instruction to wrap the base model prompts
SYSTEM_INSTRUCTION = (
    "You are a friendly English-only assistant. "
    "Do not define words—just respond conversationally."
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('prompt', '').strip()
    if not user_input:
        return jsonify(reply="(no prompt)"), 400

    # Wrap the user's input with a system instruction and dialogue format
    wrapped_prompt = (
        f"{SYSTEM_INSTRUCTION}\n\n"
        f"User: {user_input}\n"
        "Assistant:"
    )

    # Build the payload for the completions endpoint
    payload = {
        "model": MODEL,
        "prompt": wrapped_prompt,
        "max_tokens": 150,
        "temperature": 0.7
    }
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send the request to LM Studio's local API
    resp = requests.post(f"{API_BASE}/completions", json=payload, headers=headers)
    if not resp.ok:
        return jsonify(error=f"{resp.status_code} {resp.text}"), 500

    # Extract the assistant's reply from the response
    body = resp.json()
    text = body.get("choices", [{}])[0].get("text", "").strip()
    return jsonify(reply=text)

if __name__ == '__main__':
    # Run the Flask development server
    app.run()
