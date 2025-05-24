# Пример поиска
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
index = faiss.read_index("../vector_db/celeste_vector_db.index")
with open("../vector_db/text_blocks.json", "r", encoding="utf-8") as f:
    text_blocks = json.load(f)

query = "How can i do a corner jump?"
query_embedding = model.encode([query])
D, I = index.search(query_embedding, k=3)

for i in I[0]:
    print(f"Схожий блок: {text_blocks[i]['title']}")