# lmstudio-promptfoo-chatbot

A self-hosted web chatbot powered by LM Studio and tested with Promptfoo.  
Talk to a local LLM in your browser, then run an automated red-team suite to probe for safety issues.

---

## Features

- 🔌 **Local LLM**: Uses LM Studio’s OpenAI-compatible API on `http://localhost:1234/v1`  
- 🌐 **Web UI**: Simple Flask app with a chat window  
- 🛡️ **Red-teaming**: Promptfoo config ready to generate and evaluate adversarial prompts  

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

---

## AI Red-Teaming with Promptfoo

We’ve included a `promptfooconfig.yaml` that:

- Defines your travel-agent prompt template  
- Targets the local `/v1/completions` endpoint  
- Runs 5 tests each for bias, hallucination, cybercrime, PII leaks, unsafe-practice checks  
- Uses basic + jailbreak strategies  

### Run a full red-team cycle:

~~~bash
# generate adversarial inputs
promptfoo redteam generate

# evaluate against your local model
promptfoo redteam run

# view an interactive report
promptfoo redteam report
~~~

---
