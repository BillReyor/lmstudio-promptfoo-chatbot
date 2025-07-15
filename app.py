import os
import requests
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
API_KEY  = os.getenv("OPENAI_API_KEY", "dummy-key")
MODEL    = "colossal-llama-2-7b-base"

SYSTEM_INSTRUCTION = (
    "You are a helpful and friendly creative writing assistant. "
    "Respond only in English and keep interactions safe and respectful. "
    "Politely decline requests for harmful or unethical content."
)

@app.route('/')
def home():
    session.setdefault('history', [])
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('prompt', '').strip()
    if not user_input:
        return jsonify(reply="(no prompt)"), 400

    history = session.get('history', [])

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
        "temperature": 0.7,
        "stop": ["User:"]
    }
    headers = {
        "Content-Type":  "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    resp = requests.post(f"{API_BASE}/completions", json=payload, headers=headers)
    if not resp.ok:
        return jsonify(error=f"{resp.status_code} {resp.text}"), 500

    body = resp.json()
    text = body.get("choices", [{}])[0].get("text", "")

    if "User:" in text:
        text = text.split("User:")[0]
    text = text.replace("Assistant:", "").strip()

    history.append({'user': user_input, 'assistant': text})
    session['history'] = history

    return jsonify(reply=text)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('history', None)
    return jsonify(status="history cleared")

if __name__ == '__main__':
    app.run()
