import os
from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# 1. Configure OpenAI to hit LM Studio
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "colossal-llama-2-7b-base"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify(reply="(no prompt)"), 400

    # 2. Call the completions endpoint
    resp = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    text = resp.choices[0].text.strip()
    return jsonify(reply=text)

if __name__ == '__main__':
    # 3. Run on localhost:5000
    app.run(debug=True)
