# streamlit_app/main.py
import streamlit as st
from pathlib import Path

# Добавляем корневую папку проекта в sys.path, чтобы можно было импортировать rag_components
import sys
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))

from rag_components.logic.llm import get_model
from rag_components.logic.retrieval import build_vectorstore

st.set_page_config(page_title="Celeste RAG Chatbot", layout="wide")

# --- Sidebar для API‑ключей ---
with st.sidebar:
    st.markdown("### Configuration")
    gigachat_key = st.text_input("GigaChat API Key", type="password")
    st.markdown(
        "[View the source code on GitHub](https://github.com/Skillet323/Games_RAG)",
        unsafe_allow_html=True
    )

# --- Заголовок + приветственное сообщение ---
st.title("Celeste Chatbot (RAG‑Powered)")
st.caption("Ask me anything about Celeste. I’ll find relevant wiki pages and answer in ≤3 sentences.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am your Celeste assistant. Ask me anything about Celeste."}
    ]

# Рендерим чат‑историю
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Построение (или загрузка) FAISS индекса один раз при старте ---
@st.cache_resource(show_spinner=False)
def load_retriever():
    return build_vectorstore().as_retriever(search_kwargs={"k": 3})

retriever = load_retriever()

# --- Когда пользователь отправил новый запрос ---
if prompt := st.chat_input("Type your Celeste question here..."):
    if not gigachat_key:
        st.warning("Please paste your GigaChat API key in the sidebar before continuing.")
        st.stop()

    # Добавляем сообщение пользователя в сессию
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # 1) Получаем топ‑3 документа из FAISS
    docs = retriever.get_relevant_documents(prompt)
    if not docs:
        context_block = "No relevant Celeste pages found."
    else:
        # Собираем тексты трёх документов через двойной перенос строки
        context_block = "\n\n".join([doc.page_content for doc in docs])

    # 2) Формируем RAG‑промпт: Question + Context
    full_prompt = f"Question: {prompt}\nContext: {context_block}"

    # 3) Теперь собираем список сообщений для GigaChat,
    messages_to_gigachat = [
        {"role": "system", "content": "Отвечай на языке запроса пользователя."},
        {"role": "user", "content": full_prompt}
    ]

    # 4) Вызываем GigaChat с двумя сообщениями (system + user)
    model = get_model()
    response = model.invoke(messages_to_gigachat)
    answer = response.content.strip()

    # Сохраняем и выводим ответ ассистента
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
