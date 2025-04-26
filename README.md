Of course! Here's **everything cleaned up into a single full `README.md` file**, ready for you to paste directly:

```markdown
# BandWiki.AI - AC/DC QA API

A **FastAPI** service for **retrieval-augmented question answering (RAG)** about the band **AC/DC**, powered by **ChromaDB**, **HuggingFace Embeddings**, and **OpenRouter Gemini** models.

This project is designed to be **modular**, **scalable**, and **expandable** to other musical bands or encyclopedic topics in the future.

---

## ✨ Features

- **FastAPI** backend for high-performance APIs
- **ChromaDB** for local persistent vector storage
- **HuggingFace Sentence Transformers** (`intfloat/e5-large-v2`) for high-quality text embeddings
- **OpenRouter Gemini (or any LLM)** for natural language reasoning and answering
- **Retrieval-Augmented Generation (RAG)**: uses real documents to ground the LLM's responses
- **Session-based memory** using LangChain's message history for conversational continuity
- **LangChain Tool-calling Agents**: modular design to easily add more tools
- **Prompt engineering** to strictly control LLM behavior (no hallucinations)

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Youssef-Malek2004/BandWiki.AI.git
cd BandWiki.AI
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
# Edit the .env file and add your OpenRouter or OpenAI API keys
```

### 4. Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:  
`http://127.0.0.1:8000/`

---

## 📚 API Endpoints

| Method | Endpoint         | Description                                 |
|:------:|:-----------------:|:--------------------------------------------|
| `GET`  | `/healthcheck`    | Health check to verify API is running       |
| `POST` | `/query`          | Submit a question about AC/DC               |

### Example `POST /query`

```json
{
  "query": "List AC/DC albums.",
  "session_id": "user123"
}
```

- `query`: Natural language question about AC/DC.
- `session_id`: Unique ID for maintaining chat history.

**Response example:**

```json
{
  "result": "Some of AC/DC's albums include: High Voltage, Highway to Hell, Back in Black..."
}
```

---

## 🗂️ Project Structure

```plaintext
app/
│
├── agent.py          # Defines the agent, memory, and invocation logic
├── chroma_store.py   # Handles ChromaDB vector database setup
├── tools.py          # Defines custom retrieval tools
├── prompts/
│   └── acdc_prompt.py  # Stores prompt templates for modularity
├── config.py         # Environment and model configurations
├── models.py         # Request and response data schemas
└── main.py           # FastAPI application entry point
```

---

## 🛠️ Future Plans

- Expand to support more bands and music-related queries
- Add band "profiles" for artists, discographies, and timelines
- Enhance retrieval with more fine-grained document chunking
- Deploy a public API version with caching and monitoring

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🏷️ Badges

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green)](https://fastapi.tiangolo.com/)  
[![LangChain](https://img.shields.io/badge/langchain-0.1+-purple)](https://langchain.dev/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

---

## 🌟 Credits

- [ChromaDB](https://docs.trychroma.com/)
- [HuggingFace Sentence Transformers](https://www.sbert.net/)
- [LangChain Framework](https://www.langchain.dev/)
- [OpenRouter / OpenAI](https://openrouter.ai/)

---

# Thanks for checking out **BandWiki.AI**!