# rag_components/logic/llm.py
from dotenv import load_dotenv
from pathlib import Path
import os
from langchain_gigachat import GigaChat
from langchain_core.language_models import BaseChatModel

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_model(model_name: str = "GigaChat-2") -> BaseChatModel:
    """
    Instantiates a GigaChat-based chat model using credentials from .env.
    """
    api_key = os.getenv("GIGACHAT_AUTHORIZATION_KEY")
    if not api_key:
        raise ValueError("GIGACHAT_AUTHORIZATION_KEY not found in .env")

    giga = GigaChat(
        credentials=api_key,
        verify_ssl_certs=False,
        scope="GIGACHAT_API_PERS",
        model=model_name
    )
    return giga
