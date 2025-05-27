from dotenv import dotenv_values
from langchain_gigachat import GigaChat
from langchain_core.language_models import BaseChatModel



def get_model(model_name: str="GigaChat-2") -> BaseChatModel:

    config = dotenv_values("D:\Torch\Games_RAG\.env")

    giga = GigaChat(
    credentials=config["GIGACHAT_AUTHORIZATION_KEY"],
    verify_ssl_certs=False,
    scope="GIGACHAT_API_PERS",
    model=model_name
    )
    return giga
