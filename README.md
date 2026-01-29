# 🤖 Toolkit-AI — Multi-Tool LLM Agent Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

Toolkit-AI is a **production-oriented, Streamlit-based multi-tool LLM agent framework** designed for developers and researchers who want to experiment with **LLM + tool orchestration**, rapid prototyping, and interactive AI assistants.

This project integrates **OpenAI-compatible LLM providers** (AI Pipe, OpenRouter, OpenAI-style endpoints) with a curated toolbox of reusable utilities such as search, summarization, file analysis, CSV processing, and code execution.

---

## 📑 Table of Contents

- [Purpose & Goals](#-purpose--goals)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Tool System](#-tool-system)
- [API Reference](#-api-reference)
- [Examples](#-examples)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Purpose & Goals

### Purpose

- Provide a **local developer sandbox** for building and testing tool-enabled LLM workflows
- Enable rapid experimentation with **agent-based architectures**
- Serve as a **base template** for building custom AI assistants
- Bridge the gap between prototype and production-ready AI applications

### Goals

- Simple **Streamlit web UI** to interact with LLM + tools
- **Modular design** so tools can be easily added or removed
- **LLM-provider agnostic** architecture
- **Production-oriented** project structure (not just a demo)
- **Developer-friendly** with clear documentation and examples

### Who Is This For?

| Audience | Use Case |
|----------|----------|
| 🧑‍💻 Developers | Build custom AI assistants and chatbots |
| 🔬 Researchers | Experiment with LLM + tool architectures |
| 📚 Students | Learn about AI agents and tool orchestration |
| 🏢 Enterprises | Prototype internal AI tools quickly |

---

## ✨ Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Tool LLM Agent** | Intelligent tool selection and orchestration |
| 🔌 **OpenAI-Compatible** | Works with AI Pipe, OpenRouter, OpenAI, Azure OpenAI |
| 🧰 **25+ Built-in Tools** | Search, summarization, code execution, and more |
| 🖥️ **Streamlit UI** | Beautiful, interactive web interface |
| 📂 **File Analysis** | PDF, DOCX, CSV, TXT, JSON, XML support |
| 📊 **Data Analysis** | CSV processing, visualization, statistics |
| 💻 **Code Execution** | Sandboxed Python execution (dev-only) |
| 🧩 **Extensible** | Easy to add custom tools |
| 🔄 **Conversation Memory** | Maintains context across interactions |
| 📝 **Chat History** | Export and save conversations |

### Advanced Features

| Feature | Description |
|---------|-------------|
| 🔀 **Multi-Step Reasoning** | Chain multiple tools for complex tasks |
| 🎛️ **Model Selection** | Switch between different LLM models |
| 📈 **Token Tracking** | Monitor API usage and costs |
| 🌐 **Web Scraping** | Extract content from websites |
| 🔍 **Semantic Search** | Find relevant information quickly |
| 📧 **Email Integration** | Send emails via SMTP (optional) |
| 🗄️ **Database Queries** | Connect to SQL databases (optional) |

---

## 🏗️ Architecture

### High-Level Overview
