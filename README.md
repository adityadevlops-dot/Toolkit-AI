# 🤖 Multi-Tool LLM Agent

A production-oriented, Streamlit-based multi-tool LLM agent that integrates OpenAI-compatible LLM clients with a comprehensive toolbox of 25+ reusable utilities. Perfect for exploring tool-enabled LLM workflows, rapid prototyping, and building interactive AI assistants.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Available Tools](#-available-tools)
- [Extending the Toolset](#-extending-the-toolset)
- [Security](#-security--sandboxing)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **🎯 25+ Built-in Tools**: Calculator, Web Search, Weather, Wikipedia, File Reader, Code Executor, CSV Analyzer, and more
- **🔄 Multiple LLM Support**: Compatible with OpenAI, AI Pipe, OpenRouter, and any OpenAI-compatible endpoint
- **🎨 Interactive Web UI**: Streamlit-based interface with categorized tools and real-time responses
- **🔌 Modular Architecture**: Easy to add, remove, or customize tools
- **📁 Multi-Format Support**: PDF, DOCX, TXT, CSV, JSON, and more
- **💾 Vector Store Integration**: Built-in semantic search capabilities
- **🛡️ Sandboxed Execution**: Safe code execution environment

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- An API token for an OpenAI-compatible LLM service (AI Pipe, OpenRouter, or OpenAI)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/multi_tool_llm_agent.git
cd multi_tool_llm_agent
```

2. **Create and activate a virtual environment**

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:

```env
AIPIPE_API_KEY=your_api_key_here
# Optional settings:
AIPIPE_BASE_URL=https://api.aipipe.org
DEFAULT_MODEL=gpt-4o-mini
MAX_TOKENS=1024
TEMPERATURE=0.2
VERBOSE=true
```

5. **Run the application**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
multi_tool_llm_agent/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration and environment settings
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── README.md                # This file
│
├── agent/                   # Core orchestration modules
│   ├── __init__.py
│   ├── agent.py            # Agent orchestration and tool selection
│   ├── llm_client.py       # LLM client wrapper (OpenAI-compatible)
│   └── aipipe_client.py    # AI Pipe specific implementation
│
├── tools/                   # Tool implementations (25+ tools)
│   ├── __init__.py
│   ├── base_tool.py        # Base tool interface
│   ├── calculator.py       # Math operations
│   ├── web_search.py       # Web search integration
│   ├── weather.py          # Weather information
│   ├── wikipedia.py        # Wikipedia queries
│   ├── file_reader.py      # Multi-format file reading
│   ├── csv_analyzer.py     # CSV analysis
│   ├── code_executor.py    # Python code execution
│   ├── code_generator.py   # Code generation
│   ├── text_summarizer.py  # Text summarization
│   ├── code_debugger.py    # Code debugging assistance
│   ├── url_reader.py       # Web content extraction
│   ├── semantic_qa.py      # Semantic question answering
│   ├── task_planner.py     # Task planning
│   ├── translator.py       # Language translation
│   ├── json_schema_generator.py
│   ├── regex_tool.py       # Regular expression helper
│   ├── log_analyzer.py     # Log file analysis
│   ├── email_writer.py     # Email composition
│   └── ... (and more)
│
├── data/                    # Data storage
│   ├── vector_store/       # Vector embeddings
│   └── vectorstore/        # Alternative vector store
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Helper functions
│
└── uploaded_files/         # User-uploaded file storage
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AIPIPE_API_KEY` | ✅ Yes | - | Your API token for the LLM service |
| `AIPIPE_BASE_URL` | ❌ No | https://api.aipipe.org | Custom endpoint URL |
| `DEFAULT_MODEL` | ❌ No | gpt-4o-mini | Default LLM model to use |
| `MAX_TOKENS` | ❌ No | 1024 | Maximum tokens in responses |
| `TEMPERATURE` | ❌ No | 0.2 | Temperature for response creativity |
| `VERBOSE` | ❌ No | false | Enable verbose logging |

### Configuration File

Edit `config.py` to modify:
- File upload size limits
- Tool categories and visibility
- Default tool settings
- Logging configuration

## 🛠️ Available Tools

### Core Tools
- **Calculator**: Solve math equations, derivatives, integrals
- **Task Planner**: Break down complex tasks into steps
- **Intent Classifier**: Categorize user requests

### AI & NLP
- **Text Summarizer**: Summarize long documents
- **Translator**: Translate between languages
- **Semantic QA**: Question answering with embeddings
- **Email Writer**: Generate professional emails

### Developer Tools
- **Code Generator**: Generate code from descriptions
- **Code Executor**: Run Python code safely
- **Code Debugger**: Debug and explain code
- **Regex Tool**: Build and test regular expressions
- **API Tester**: Test REST APIs
- **Dependency Analyzer**: Analyze code dependencies
- **Unit & Currency Converter**: Convert units and currencies

### Data Tools
- **CSV Analyzer**: Analyze CSV files
- **Data Visualizer**: Create data visualizations
- **JSON Schema Generator**: Generate JSON schemas
- **Log Analyzer**: Parse and analyze logs

### Information Tools
- **Web Search**: Google-powered web search
- **URL Reader**: Extract content from websites
- **Wikipedia**: Query Wikipedia articles
- **Weather**: Get weather information
- **DateTime Reasoner**: Date/time calculations

### Utilities
- **File Reader**: Read PDF, DOCX, TXT, CSV, JSON
- **Prompt Optimizer**: Improve prompt quality
- **AI Tool**: Direct LLM interaction

## 🔌 Extending the Toolset

### Add a New Tool

1. **Create a new tool file** in `tools/`:

```python
# tools/my_tool.py
from tools.base_tool import BaseTool

class MyTool(BaseTool):
    name = "my_tool"
    description = "What this tool does"
    category = "Utilities"
    
    def execute(self, **kwargs):
        """Execute the tool with given parameters"""
        # Implementation here
        return result
```

2. **Register the tool** in `tools/__init__.py`:

```python
from tools.my_tool import MyTool

# Add to tool registry
TOOLS = {
    "my_tool": MyTool(),
    # ... other tools
}
```

3. **Update the UI** in `app.py` if needed (custom icons, descriptions, etc.)

### Best Practices

- ✅ Keep tools single-responsibility
- ✅ Validate inputs early
- ✅ Use type hints
- ✅ Add comprehensive docstrings
- ✅ Make tools idempotent
- ✅ Prefer pure functions
- ✅ Mock I/O for testing

## 🛡️ Security & Sandboxing

⚠️ **Important Security Notes**:

1. The `code_executor` tool runs Python code. Only use with trusted inputs.
2. For production, implement additional sandboxing (Docker containers, restricted VMs)
3. Validate and limit file uploads using `Config.MAX_FILE_SIZE`
4. Never expose API keys in version control
5. Use `.env` files for sensitive configuration

## 📊 Quick Test

Validate your LLM client setup with a quick smoke test:

```python
from agent.llm_client import LLMClient

client = LLMClient(api_key='your_api_key')
response = client.simple_chat('Say hello!')
print(response)
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Missing AIPIPE_API_KEY` | Create `.env` file or set environment variable |
| `Module import errors` | Ensure you're in project root and venv is activated |
| `Dependency issues` | Run `pip install --upgrade pip` then `pip install -r requirements.txt` |
| `Streamlit not found` | Check virtual environment activation |
| `LLM connection errors` | Verify API key validity and network connectivity |
| `Tool not appearing in UI` | Check tool registration in `tools/__init__.py` |

## 📝 Testing

### Unit Tests
- Mock LLM responses and tool outputs
- Keep tests isolated and small
- Use pytest for test framework

### Integration Tests
- Use test API keys or mock servers
- Test full workflows end-to-end

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Add new tools with documentation
- Include examples for inputs/outputs
- Write tests for new functionality
- Keep commits focused and descriptive
- Update README if adding major features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💼 Author

**Aditya Devlops**
- GitHub: [@adityadevlops-dot](https://github.com/adityadevlops-dot)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the excellent web framework
- [OpenAI](https://openai.com/) for the LLM API
- [AI Pipe](https://aipipe.org/) for the compatible API service
- All contributors and users who help improve this project

## 💬 Support

If you have questions or need help:

1. **Check the [Troubleshooting](#-troubleshooting) section** above
2. **Open an [Issue](../../issues)** on GitHub
3. **Check existing discussions** in the repository
4. **Read the code comments** and docstrings for detailed implementation info

---

<div align="center">

Made with ❤️ by Aditya Devlops

[⬆ Back to top](#-multi-tool-llm-agent)

</div>
