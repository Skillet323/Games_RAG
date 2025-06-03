# rag_components/logic/retrieval.py
import json
import os
from pathlib import Path

# Рекомендуется сразу перейти на langchain_community, чтобы не получать DeprecationWarning:
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain.docstore.document import Document
from langchain.tools.retriever import create_retriever_tool

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / "scrapy_project" / "output" / "combined_clean.jl"
VECTORSTORE_DIR = PROJECT_ROOT / "models" / "faiss_index"

def build_vectorstore() -> FAISS:
    """
    Строит (или загружает) FAISS-индекс всех документов из `combined_clean.jl`.
    При загрузке устанавливаем allow_dangerous_deserialization=True, 
    чтобы разрешить десериализацию собственной базы (pickle).
    """
    VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

    if (VECTORSTORE_DIR / "index.faiss").exists():
        # Если индекс уже сохранён, загружаем его с флагом allow_dangerous_deserialization=True
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectordb = FAISS.load_local(
            str(VECTORSTORE_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectordb

    # Иначе: читаем JSONL, собираем список Document и индексируем
    docs = []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            text = data.get("full_text", "").strip()
            title = data.get("title", "").strip()
            if not text:
                continue
            docs.append(Document(page_content=text, metadata={"title": title}))

    if not docs:
        raise RuntimeError(f"No documents found in {DATA_PATH} to build vectorstore.")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embeddings)
    vectordb.save_local(str(VECTORSTORE_DIR))
    return vectordb

def get_retriever_tool():
    """
    Возвращает LangChain Tool, который при вызове отдаёт топ‑3 наиболее релевантных
    фрагмента о Celeste из FAISS.
    """
    vectordb = build_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    retriever_tool = create_retriever_tool(
        retriever,
        name="retrieve_celeste_info",
        description="Search and return the top 3 most relevant passages about Celeste."
    )
    return retriever_tool
