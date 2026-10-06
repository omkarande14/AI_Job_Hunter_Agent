# Autonomous AI Job Discovery & Evaluation Agent

An autonomous agentic workflow combining **live web search** (DuckDuckGo Search) and **local LLM reasoning** (Ollama + Llama 3 8B via LangChain) to discover, filter, match, and draft tailored application pitches for remote AI/ML and GenAI engineering roles.

---

## 📌 Architecture & Features

```text
[ Target Job Queries ]
         │
         ▼
[ LiveJobFetcher ] ───> DuckDuckGo Live Search API (LinkedIn, Naukri, Indeed)
         │
         ▼
[ Anti-Spam Filter ] ───> Excludes fraudulent listings (registration fees, deposits)
         │
         ▼
[ AIJobAgent ] ───> Local Ollama (Llama 3 8B) + LangChain PromptTemplate
         │
         ▼
[ Output Report ]
  ├── 🎯 Objective Match Score (0 - 100%)
  ├── 💡 Core Matching Skills
  ├── ✉️ Tailored 3-Sentence HR Pitch
  └── 🔗 Direct Apply Link
```

### Key Components

1. **`job_agent.py`**:
   - Multi-query search aggregator querying verified job listings from LinkedIn, Naukri, and Indeed.
   - Built-in anti-spam heuristics.
   - Profile-aware evaluation using LangChain's pipeline (`prompt | llm`).
2. **`llama3_terminal_chat.py`**:
   - Interactive terminal chat assistant supporting multilingual dialogue (Marathi & English) with streaming generation and conversational memory.

---

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have [Ollama](https://ollama.com/) installed and running locally with the `llama3:8b` model pulled:

```bash
ollama pull llama3:8b
ollama serve
```

### 2. Install Dependencies

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Run the Job Discovery Agent

```bash
python job_agent.py
```

### 4. Run the Interactive Chat Assistant

```bash
python llama3_terminal_chat.py
```