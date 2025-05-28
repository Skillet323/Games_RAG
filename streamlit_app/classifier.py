import json
import os
import pickle

from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


class ArticleClassifier:
    def __init__(self, model_name="all-MiniLM-L6-v2", k_neighbors=5):
        self.model = SentenceTransformer(model_name)
        self.knn = NearestNeighbors(n_neighbors=k_neighbors, metric="cosine")
        self.embeddings = None
        self.texts = []
        self.titles = []

    def load_data(self, jsonl_path):
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                text = entry.get("full_text", "").strip()
                if len(text) > 30:
                    self.texts.append(text)
                    self.titles.append(entry.get("title", "Untitled"))

    def train(self):
        print("Embedding and training on data...")
        self.embeddings = self.model.encode(self.texts, convert_to_numpy=True)
        self.knn.fit(self.embeddings)
        print("Training complete.")

    def save(self, knn_path, titles_path):
        with open(knn_path, "wb") as f:
            pickle.dump((self.knn, self.embeddings), f)
        with open(titles_path, "w", encoding="utf-8") as f:
            json.dump(self.titles, f, ensure_ascii=False)

    def load(self, knn_path, titles_path):
        with open(knn_path, "rb") as f:
            self.knn, self.embeddings = pickle.load(f)
        with open(titles_path, "r", encoding="utf-8") as f:
            self.titles = json.load(f)

    def predict(self, query, top_k=1):
        query_emb = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.knn.kneighbors(query_emb, n_neighbors=top_k)
        return [self.titles[i] for i in indices[0]]


def main():
    model_dir = "../models"
    data_path = "../scrapy_project/output/combined_clean.jl"
    os.makedirs(model_dir, exist_ok=True)

    knn_path = os.path.join(model_dir, "knn_model_clean.pkl")
    titles_path = os.path.join(model_dir, "titles.json")

    clf = ArticleClassifier()

    if not os.path.exists(knn_path) or not os.path.exists(titles_path):
        print(f"Training new model from {data_path}...")
        clf.load_data(data_path)
        clf.train()
        clf.save(knn_path, titles_path)
    else:
        print("Loading existing model...")
        clf.load(knn_path, titles_path)

    print("\nAsk your questions (type 'exit' to quit):")
    while True:
        query = input(">>> ").strip()
        if query.lower() == "exit":
            break
        results = clf.predict(query, top_k=3)
        print("Top matches:")
        for i, title in enumerate(results, 1):
            print(f"{i}. {title}")


if __name__ == "__main__":
    main()
