# streamlit_app/main.py
import streamlit as st
from pathlib import Path

# Добавляем корневую папку проекта в sys.path, чтобы можно было импортировать rag_components
import sys
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.append(str(PROJECT_ROOT))


from rag_components.workflows.rag_workflow import create_rag_graph

st.set_page_config(page_title="Celeste RAG Chatbot", layout="wide")

# --- Sidebar для API‑ключей ---
with st.sidebar:
    st.markdown("### Configuration")
    debug_mode = st.toggle("Developer Mode", 
                          help="Позволяет видеть весь список сообщений бота")
    gigachat_key = st.text_input("GigaChat API Key", type="password")
    st.markdown(
        "[View the source code on GitHub](https://github.com/Skillet323/Games_RAG)",
        unsafe_allow_html=True
    )

env_path = PROJECT_ROOT / ".env"
with open(env_path, "w") as env_file:
    env_file.write(f"GIGACHAT_AUTHORIZATION_KEY={gigachat_key}")


# --- Заголовок + приветственное сообщение ---
st.title("Celeste Chatbot (RAG‑Powered)")
st.caption("Ask me anything about Celeste. I’ll find relevant wiki pages and answer")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am your Celeste assistant. Ask me anything about Celeste."}
    ]

# Рендерим чат‑историю
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- Построение (или загрузка) futynf ---
@st.cache_resource(show_spinner=False)
def get_graph():
    return create_rag_graph()

rag_agent = get_graph()

# --- Когда пользователь отправил новый запрос ---
if prompt := st.chat_input("Type your Celeste question here..."):
    if not gigachat_key:
        st.warning("Please paste your GigaChat API key in the sidebar before continuing.")
        st.stop() 

    # Добавляем сообщение пользователя в сессию
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Вызываем GigaChat с двумя сообщениями (system + user)
    messages_to_agent = {
            "messages": [
                {
                    "role": "system",
                    "content": "Отвечай на английском"
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        }
    
    if debug_mode:
        answer = ""
        for chunk in rag_agent.stream(messages_to_agent):
            for node, update in chunk.items():
                answer += f"UPDATE FROM NODE {node}" + "\n\n"
                answer += update["messages"][-1].pretty_repr()
                answer += "\n\n"

    else:
        response = rag_agent.invoke(messages_to_agent)
        answer = response["messages"][-1].content.strip()

    # Сохраняем и выводим ответ ассистента
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant").write(answer)
