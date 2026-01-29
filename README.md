# 🤖 Toolkit-AI — Multi-Tool LLM Agent Platform

<p align="center">
  <b>A production-oriented, extensible Multi-Tool LLM Agent built with Python & Streamlit</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" />
  <img src="https://img.shields.io/badge/Streamlit-1.28%2B-red.svg" />
  <img src="https://img.shields.io/badge/LLM-OpenAI%20Compatible-green.svg" />
  <img src="https://img.shields.io/badge/Tools-25%2B-purple.svg" />
  <img src="https://img.shields.io/badge/Status-Active-success.svg" />
</p>

---

## 🌟 Overview

**Toolkit-AI** is a **Streamlit-based, multi-tool LLM agent framework** designed for developers and researchers who want to explore **LLM + tool orchestration**, rapid prototyping, and interactive AI assistants.

It supports **OpenAI-compatible APIs** such as **AI Pipe**, **OpenRouter**, and **OpenAI**, and ships with **25+ reusable tools** out of the box.

---

## 🎯 Why Toolkit-AI?

✔️ LLM-agnostic architecture  
✔️ Modular & extensible tool system  
✔️ Local developer-friendly sandbox  
✔️ Production-oriented project structure  
✔️ Clean UI with tool categorization  
✔️ Easy to add new tools or swap models  

---

## ✨ Features

- 🧠 **Multi-Tool LLM Agent**
- 🔌 **OpenAI-Compatible Providers**
- 🧰 **25+ Built-in Tools**
- 🖥️ **Interactive Streamlit UI**
- 📂 **File Upload & Analysis**
- 📊 **CSV & Data Processing**
- 💻 **Sandboxed Code Execution**
- ⚙️ **Environment-based Configuration**

---

## 🧰 Built-In Tools

| Category | Tools |
|-------|------|
| Core | Calculator, Utilities |
| AI & NLP | Summarization, Code Generation |
| Developer | Code Executor, Debug Helpers |
| Data | CSV Analyzer, File Reader |
| Web | Web Search, Wikipedia, URL Reader |

---

## 🖼️ Demo

<p align="center">
  <img src="screenshots/demo.gif" alt="Toolkit-AI Demo" width="85%" />
</p>

> 📌 _Replace `screenshots/demo.gif` with your actual demo GIF._

---

## 🧠 Architecture Diagram

```mermaid
flowchart TD
    UI[Streamlit UI] --> Agent[LLM Agent]
    Agent --> LLM[LLM Client]
    Agent --> Tools[Tool Registry]
    Tools --> Web[Web Tools]
    Tools --> Data[Data Tools]
    Tools --> Dev[Developer Tools]
    LLM --> Agent


📂 Project Structure
Toolkit-AI/
│
├── app.py                 # Streamlit UI & orchestration
├── config.py              # Configuration & defaults
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
│
├── agent/
│   ├── agent.py           # Agent orchestration logic
│   └── llm_client.py      # OpenAI-compatible LLM client
│
├── tools/
│   ├── __init__.py        # Tool registry
│   ├── calculator.py
│   ├── web_search.py
│   ├── wikipedia.py
│   ├── file_reader.py
│   ├── csv_analyzer.py
│   ├── code_executor.py
│   └── ...

---

## ⚙️ Requirements

- **Python** 3.10+
- **Streamlit** 1.28+
- **API Key** for one of the following:
  - AI Pipe
  - OpenRouter
  - Any OpenAI-compatible endpoint

---

## 🚀 Quick Start

### 1️⃣ Create Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment

Create a .env file in the project root:

AIPIPE_API_KEY=your_api_key_here

# Optional configuration
# AIPIPE_BASE_URL=https://api.aipipe.org
# DEFAULT_MODEL=gpt-4o-mini
# MAX_TOKENS=1024
# TEMPERATURE=0.2
# VERBOSE=true

4️⃣ Run the Application
streamlit run app.py


The Streamlit app will launch automatically in your browser 🚀

🔧 Configuration Options
Variable	Description
AIPIPE_API_KEY	API key (required)
AIPIPE_BASE_URL	Custom OpenAI-compatible endpoint
DEFAULT_MODEL	LLM model name
MAX_TOKENS	Maximum token limit
TEMPERATURE	Response creativity
VERBOSE	Enable debug logging
🧩 Adding New Tools

Create a new tool module inside tools/

Implement execute(**kwargs) or extend BaseTool

Register the tool in tools/__init__.py

(Optional) Add UI metadata (icon, category, description) in app.py

Best Practices

Keep tools single-responsibility

Validate inputs early

Keep logic pure and testable

Isolate I/O (web, files, APIs)

🔐 Security Notice

⚠️ Important

code_executor is intended for development only

Do NOT run untrusted code in production

Always validate uploaded file types and size limits

🧪 Quick Smoke Test

Use this to quickly verify the LLM client:

from agent.llm_client import LLMClient

client = LLMClient(api_key="your_key")
print(client.simple_chat("Say OK"))

📜 License

No license is included by default.
Add MIT or Apache-2.0 if you plan to open-source this project.

⭐ Support the Project

If you find this project useful:
⭐ Star the repository
🐛 Open issues for bugs
💡 Suggest new features

<p align="center"> <b>Built with ❤️ for developers exploring LLM + Tool ecosystems</b> </p> ```
