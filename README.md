# lmstudio-promptfoo-chatbot

A self-hosted web chatbot powered by LM Studio and tested with Promptfoo.  
Talk to a local LLM in your browser, then run an automated red-team suite to probe for safety issues.

---

## Features

- 🔌 **Local LLM**: Uses LM Studio’s OpenAI-compatible API on `http://localhost:1234/v1`  
- 🌐 **Web UI**: Simple Flask app with a chat window
- 💾 **Persistent history**: Chat logs survive page reloads until you click Reset
- 🛡️ **Promptfoo testing**: YAML configs for red-teaming either the raw LM Studio model or the Flask chatbot

---

## Prerequisites

- **Python 3.8+**  
- **LM Studio** installed and running  
  - Load your model (e.g. `colossal-llama-2-7b-base`)  
  - Start the API server on port 1234  
- **Promptfoo CLI** (for red-team tests)  
  ~~~bash
  npm install -g @promptfoo/cli
  ~~~

---

## Installation

1. **Clone this repo**  
   ~~~bash
   git clone https://github.com/your-org/lmstudio-promptfoo-chatbot.git
   cd lmstudio-promptfoo-chatbot
   ~~~

2. **(Optional) Create a virtualenv**  
   ~~~bash
   python -m venv .venv
   source .venv/bin/activate
   ~~~

3. **Install Python deps**  
   ~~~bash
   pip install flask openai
   ~~~

---

## Configuration

Set these env vars so the OpenAI SDK points at your local LM Studio:

~~~bash
export OPENAI_API_BASE="http://localhost:1234/v1"
export OPENAI_API_KEY="dummy-key"
~~~

> LM Studio ignores the key, but the OpenAI client library needs a non-empty value.

---

## Running the Web Chatbot

1. **Start Flask**  
   ~~~bash
   export FLASK_APP=app.py
   flask run
   ~~~

2. **Open your browser** at [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. **Chat away!** Type a message and hit Send to get a reply from your local model.
4. Use **Reset Conversation** to clear the history if needed

---

## AI Red-Teaming with Promptfoo

This repo ships with three ready-made Promptfoo configs so you can evaluate either the LM Studio API directly or the Flask chatbot:

- `promptfooconfig.yaml` – example red-team setup for `http://localhost:1234/v1`
- `test-1-lmstudio.yaml` – calls the `/v1/completions` endpoint without the Flask app
- `test-2-chatbot-app.yaml` – sends tests to the `/chat` route of this web app

### Run a full red-team cycle

Use `promptfooconfig.yaml` for a complete red-team workflow:

~~~bash
# generate adversarial inputs
promptfoo redteam generate

# evaluate against your local model
promptfoo redteam run

# view an interactive report
promptfoo redteam report
~~~

For quick tests you can run the other configs directly:

~~~bash
# hit LM Studio directly
promptfoo eval test-1-lmstudio.yaml

# test the Flask chatbot API
promptfoo eval test-2-chatbot-app.yaml
~~~

---
