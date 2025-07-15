import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI  # new SDK import

app = Flask(__name__)

# 1. Instantiate the new client with your LM Studio settings
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_API_BASE")
)

MODEL = "colossal-llama-2-7b-base"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    if not prompt:
        return jsonify(reply="(no prompt)"), 400

    try:
        # 2. Use the new completions endpoint
        resp = client.completions.create(
            model=MODEL,
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        text = resp.choices[0].text.strip()
        return jsonify(reply=text)

    except Exception as e:
        # 3. Surface any errors back to the client for easy debugging
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run()
