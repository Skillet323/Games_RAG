import streamlit as st

# Это боковая панель для ввода ключа
with st.sidebar:
    gigachat_api_key = st.text_input("GigaChat API Key", key="gigachat_api_key", type="password")

    "[View the source code](https://https://github.com/Skillet323/Games_RAG)"


st.title("Celeste Chatbot")
st.caption("For any questions regarding Celeste")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! I am ChatBot that was created to answer Celeste questions"}]

# Вывод всех сообщений
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Ответ на вопрос
if prompt := st.chat_input():
    # Проверку на ключ пока убрал, чтобы проще тестировать
    # if not gigachat_api_key:
    #     st.info("Please add your key to continue.")
    #     st.stop()

    client = ... # тут будет наш агент
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = ... # а здесь вызов  агента
    msg = "Not Implemented"
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
