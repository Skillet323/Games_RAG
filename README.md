## Celeste Knowledge Assistant 🏔️

A Retrieval-Augmented Generation (RAG) system designed to answer questions about the critically acclaimed game *Celeste*. This project combines web scraping with large language models to provide accurate information about game mechanics, story elements, and technical details.

## Project Structure 📂

```
GAMES_RAG/
│
├── scrapy_project/ # Data collection and processing
│
├── streamlit_app/ # Web interface
│
└── rag_components/ # Parts of the rag itself

```

## Components 🛠️

### 1. Data Collection (`scrapy_project/`)

Responsible for building the knowledge base by scraping:
- celeste.ink
- celestegame.fandom.wiki

**Setup & Usage:**
```bash
cd scrapy_project
scrapy crawl celeste -o output/celeste_pages.jl
```

### 2. Web Interface (`streamlit_app/`)

Interactive application featuring:

- Natural language question answering
- Source citations
- Visual examples
- Conversation history

**Setup & Usage:**

```bash
cd streamlit_app
streamlit run main.py
```