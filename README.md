# 🤖 Toolkit-AI — Multi-Tool LLM Agent Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Contributors](https://img.shields.io/github/contributors/adityadevlops-dot/Toolkit-AI)](https://github.com/adityadevlops-dot/Toolkit-AI/graphs/contributors)
[![Repo Size](https://img.shields.io/github/repo-size/adityadevlops-dot/Toolkit-AI)](https://github.com/adityadevlops-dot/Toolkit-AI)

Toolkit-AI is a production-oriented, Streamlit-based multi-tool LLM agent framework designed to help developers, researchers, and teams build, test, and deploy tool-enabled LLM workflows quickly and safely.

---

Table of Contents
- [Why Toolkit-AI](#why-toolkit-ai)
- [Highlights](#highlights)
- [Architecture](#architecture)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Usage](#usage)
- [Tools & Integrations](#tools--integrations)
- [Security & Safety](#security--safety)
- [Deployment & Monitoring](#deployment--monitoring)
- [Development & Contributing](#development--contributing)
- [Roadmap](#roadmap)
- [License & Credits](#license--credits)
- [Contact](#contact)

---

## Why Toolkit-AI

Toolkit-AI was built to:
- Provide a secure local sandbox for building agent-based LLM workflows.
- Enable rapid experimentation with tool orchestration and multi-step reasoning.
- Serve as a clean, production-minded reference implementation that is extensible and auditable.

Use cases:
- Building assistants that combine search, file analysis, web scraping, and code execution.
- Researching multi-step decision-making with tool calls.
- Prototyping internal automation pipelines that must be auditable and configurable.

---

## Highlights

- 🧠 Multi-tool LLM orchestration — intelligently select and chain tools.
- 🔌 OpenAI-compatible — supports AI Pipe, OpenRouter, OpenAI-style endpoints.
- 🧰 25+ built-in tools for search, summarization, file analysis, and more.
- 🖥️ Streamlit UI — fast development UI with chat, tool cards, and analytics.
- 📂 File analysis (PDF/DOCX/CSV/JSON/TXT) and semantic search.
- 💻 Optional sandboxed Python execution (developer mode).
- 🔐 Focus on security: API key isolation, optional network sandboxing, prompt auditing.
- 🚀 Production-aware structure: config driven, pluggable backends, token/cost tracking.

---

## Architecture

A high-level architecture view (Mermaid):

```mermaid
flowchart TD
  A[User (Browser)] -->|Streamlit UI| B[Toolkit-AI Frontend]
  B --> C[Agent Orchestrator]
  C -->|calls| D[Toolbox]
  D --> D1[Search Service]
  D --> D2[File Processor]
  D --> D3[Code Runner]
  D --> D4[External APIs]
  C -->|requests| E[LLM Provider]
  E -->|responses| C
  C -->|logs| F[Audit & Metrics]
  F --> G[Monitoring / Billing]
  style A fill:#f9f,stroke:#333,stroke-width:1px
  style F fill:#eef,stroke:#333,stroke-width:1px
```

Components:
- Streamlit UI: chat interface, tool management, settings.
- Agent Orchestrator: handles reasoning, tool selection, and execution flow.
- Toolbox: pluggable tool implementations (search, scrape, file analysis, DB).
- LLM Provider: OpenAI-compatible endpoint. Swappable to other providers.
- Audit & Metrics: conversation history, prompt & tool logs, cost metrics.

---

## Quickstart

Prerequisites:
- Python 3.10+
- Git
- (Optional) Virtualenv / Conda

Clone & run locally:

```bash
git clone https://github.com/adityadevlops-dot/Toolkit-AI.git
cd Toolkit-AI

# Create venv (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\activate     # Windows

pip install -U pip
pip install -r requirements.txt

# Create .env (see Configuration below)
cp .env.example .env
# edit .env with your API keys & settings

# Start Streamlit UI
streamlit run app.py
# or if the main entry is `streamlit_app.py`, run:
# streamlit run streamlit_app.py
```

First-time tips:
- Use a low-cost LLM for early testing.
- Turn off any sandboxed code execution unless you control the environment.
- Check the "Developer" panel for logs and token usage.

---

## Configuration

Toolkit-AI uses environment variables and a config file to control runtime behavior.

Example .env (sensitive values must be stored securely):

```env
# .env.example
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1
DEFAULT_MODEL=gpt-4o-mini
STREAMLIT_SERVER_PORT=8501
ENABLE_CODE_EXECUTION=false
LOG_LEVEL=INFO
DB_URL=sqlite:///./toolkitai.db
```

Important configs:
- OPENAI_API_KEY / OPENAI_BASE_URL — credentials and provider endpoint.
- ENABLE_CODE_EXECUTION — set to false in production unless sandboxed.
- DB_URL — database for conversation history & metrics.

Secrets management:
- Use a secrets manager or GitHub Actions secrets for CI/CD.
- Do NOT commit API keys or credentials to the repository.

---

## Usage

User flows:
- Chat: Interact with the agent; it will call tools as needed.
- File upload: Upload PDF/CSV/DOCX — agent will extract and index content.
- Tool debugger: Inspect the tool call chain and intermediate states.
- Export: Save chat transcripts and tool logs for auditing.

Examples

1) Summarize a PDF
- Upload the PDF in Files.
- Ask: "Summarize the key findings from the uploaded PDF and extract action items."

2) Data analysis from CSV
- Upload CSV, then ask: "Provide summary statistics and a quick visualization for column X."

3) Multi-step task (example sequence)
- User: "Plan a two-week marketing campaign for product X."
- Agent: (1) use search tool to gather references; (2) call summarizer; (3) draft campaign plan; (4) produce calendar and assets.

API / CLI
- The repository includes helper scripts (e.g., tools/cli.py) — run them for headless interactions.
- Example curl (if web API is exposed — adapt to your server):
```bash
curl -X POST "http://localhost:8501/api/chat" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"Summarize the uploaded documents"}'
```

---

## Tools & Integrations

Built-in tool types:
- Semantic Search (vector store)
- Web Scraper (HTML extraction + text cleaning)
- Document Processor (PDF / DOCX / TXT / CSV / JSON)
- Code Runner (sandboxed Python; dev mode)
- Email (SMTP)
- SQL Query Executor (optional DB connector)
- External API connector (pluggable via adapter)

Extending tools:
- Add a new tool by creating a tool class conforming to the Tool interface (see docs / tools/README).
- Register new tools in the toolbox registry (config / registry file).

---

## Security & Safety

This project is designed with security in mind, but there are risks when executing code or calling external endpoints.

Best practices:
- Never enable code execution in an untrusted environment.
- Limit network access for tool processes using OS-level network policies or containers.
- Redact and audit prompts that contain sensitive information.
- Use role-based access for any deployed instance (auth layer in front of Streamlit).
- Rotate API keys regularly and use least-privilege credentials.

Auditing:
- All tool calls and prompts are logged to the audit DB by default (configurable).
- Export logs for compliance and debugging.

---

## Deployment & Monitoring

Deploy patterns:
- Docker: Build an image and run in a containerized environment:
  - Use multi-stage builds, non-root user, and pinned dependency versions.
- Kubernetes: Deploy with a Deployment + Service; use Secrets for API keys.
- Cloud: Deploy Streamlit behind a reverse proxy (NGINX) and enable HTTPS.

Monitoring:
- Integrate with Prometheus / Grafana for metrics.
- Export token usage and cost metrics to your billing dashboard.
- Configure alerts on error rates or high-latency tool calls.

Example Docker (simplified):
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install -U pip && pip install -r requirements.txt
COPY . .
ENV STREAMLIT_SERVER_PORT=8501
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
```

---

## Development & Contributing

We welcome contributions! Please follow the guidelines below.

- Read the code of conduct and contributing guide.
- Open issues for bugs or feature requests.
- For code changes, open a Pull Request with:
  - Clear description & motivation
  - Tests where applicable
  - Updated docs

Suggested workflow:
1. Fork the repo
2. Create a feature branch: feature/your-feature
3. Run tests and linters
4. Open PR against main with detailed description and screenshots

Files of interest:
- app.py / streamlit_app.py — Streamlit entrypoint
- tools/ — implementable tool adapters
- core/agent.py — orchestrator implementation
- docs/ — documentation and examples

Code style:
- Black, isort, flake8 / pylint recommended.
- Add unit tests for logic-heavy components.

---

## Roadmap

Planned improvements:
- Role-based authentication + RBAC
- Official Docker images and Helm charts
- OAuth integrations (Google, SSO)
- Enhanced ML ops: model versioning and canary deployments
- More tool adapters (Slack, Jira, GitHub automation)

Contributions to roadmap welcome — open issues and label them with roadmap.

---

## Troubleshooting

Common issues:
- Model connection failures: check OPENAI_BASE_URL and network rules.
- File upload errors: validate file size and supported formats.
- High token usage: enable summarization & chunking, switch to lower-cost model for drafts.

Check logs:
- Local logs are printed to console / streamlit logs.
- Database (DB_URL) stores audit trails if enabled.

---

## Acknowledgements & Resources

- Inspired by agent frameworks and tool-augmented LLM research.
- Uses open-source libraries — check requirements.txt for full attributions.

Useful links:
- Streamlit: https://streamlit.io
- OpenAI API docs: https://platform.openai.com/docs
- Best practices for prompt engineering: https://github.com/dair-ai/Prompt-Engineering-Guide

---

## License & Credits

Toolkit-AI is released under the MIT License. See LICENSE for full terms.

Authors
- Maintainer: adityadevlops-dot
- Contributors: see the GitHub contributors graph

---

## Contact

For questions, feature requests, or security reports:
- Open an issue at: https://github.com/adityadevlops-dot/Toolkit-AI/issues
- Or email: your-team@example.com (replace with an appropriate contact)

---

Thank you for using Toolkit-AI — if you want, I can push this README to the repository directly (create a commit on main). Tell me if you'd like a commit message and whether to create a branch or push straight to main.
