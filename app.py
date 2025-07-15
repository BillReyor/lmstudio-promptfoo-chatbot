# app.py
import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

# Configuration from environment variables
API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
API_KEY  = os.getenv("OPENAI_API_KEY", "dummy-key")
MODEL    = "colossal-llama-2-7b-base"

# System instruction for the base model
SYSTEM_INSTRUCTION = (
    "You are a friendly English-only assistant. "
    "Do not define words—just respond conversationally."
)

@app.route('/')
def home():
    # Ensure history exists
    session.setdefault('history', [])
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('prompt', '').strip()
    if not user_input:
        return jsonify(reply="(no prompt)"), 400

    history = session.get('history', [])

    # Build the full prompt including conversation history
    prompt_lines = [SYSTEM_INSTRUCTION, ""]
    for turn in history:
        prompt_lines.append(f"User: {turn['user']}")
        prompt_lines.append(f"Assistant: {turn['assistant']}\n")
    prompt_lines.append(f"User: {user_input}")
    prompt_lines.append("Assistant:")
    wrapped_prompt = "\n".join(prompt_lines)

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

    resp = requests.post(f"{API_BASE}/completions", json=payload, headers=headers)
    if not resp.ok:
        return jsonify(error=f"{resp.status_code} {resp.text}"), 500

    body = resp.json()
    reply_text = body.get("choices", [{}])[0].get("text", "").strip()

    # Update history
    history.append({'user': user_input, 'assistant': reply_text})
    session['history'] = history

    return jsonify(reply=reply_text)

@app.route('/reset', methods=['POST'])
def reset():
    # Clear only the conversation history
    session.pop('history', None)
    return jsonify(status="history cleared")

if __name__ == '__main__':
    app.run()
