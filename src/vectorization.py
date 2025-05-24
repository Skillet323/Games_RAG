import json
import re
import logging
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Конфигурация
CONFIG = {
    "input_file": "../data/celeste_pages2.txt",
    "output_dir": "../vector_db",
    "model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "min_text_length": 20,  # Минимальная длина текста для добавления в БД
}

def load_data(file_path):
    """Загрузка данных из JSONL-файла"""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f):
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                logger.warning(f"Ошибка JSON на строке {line_num}: {e}")
    return data

def extract_text_blocks(data):
    """Извлечение текстовых блоков из данных"""
    text_blocks = []
    for entry in data:
        if "full_text" in entry and len(entry["full_text"]) > CONFIG["min_text_length"]:
            text_blocks.append({
                "text": clean_text(entry["full_text"]),
                "title": entry.get("title", "Unknown"),
                "url": entry.get("url", "")
            })
        elif "chunks" in entry:
            for chunk in entry["chunks"]:
                if len(chunk["text"]) > CONFIG["min_text_length"]:
                    text_blocks.append({
                        "text": clean_text(chunk["text"]),
                        "title": entry.get("title", "Unknown"),
                        "url": entry.get("url", "")
                    })
    logger.info(f"Извлечено {len(text_blocks)} текстовых блоков")
    return text_blocks

def clean_text(text):
    """Очистка текста от лишних символов"""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([^\w\s])", r"\1", text)
    return text

def generate_embeddings(text_blocks, model_name):
    """Генерация эмбеддингов с помощью Sentence-BERT"""
    logger.info(f"Загрузка модели {model_name}")
    model = SentenceTransformer(model_name)
    
    texts = [block["text"] for block in text_blocks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    return embeddings

def create_vector_db(embeddings, output_dir):
    """Создание и сохранение векторной БД"""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    faiss.write_index(index, str(output_dir / "celeste_vector_db.index"))
    logger.info(f"Индекс FAISS сохранен в {output_dir / 'celeste_vector_db.index'}")

def save_text_blocks(text_blocks, output_dir):
    """Сохранение текстовых блоков с метаданными"""
    output_path = Path(output_dir) / "text_blocks.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(text_blocks, f, ensure_ascii=False, indent=2)
    logger.info(f"Текстовые блоки сохранены в {output_path}")

    

def main():
    # Загрузка данных
    data = load_data(CONFIG["input_file"])
    
    # Извлечение текстовых блоков
    text_blocks = extract_text_blocks(data)
    
    # Генерация эмбеддингов
    embeddings = generate_embeddings(text_blocks, CONFIG["model_name"])
    
    # Создание векторной БД
    create_vector_db(embeddings, CONFIG["output_dir"])
    
    # Сохранение текстовых блоков
    save_text_blocks(text_blocks, CONFIG["output_dir"])


if __name__ == "__main__":
    main()

    
    