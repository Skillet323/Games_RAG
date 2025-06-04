# streamlit_app/classifier.py
import json
import joblib
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd

def convert_to_training_data(input_path, output_path):
    """
    Reads JSONL from `input_path` (each line has 'title' and 'full_text'),
    filters out empty titles/texts, and writes lines of {"text": <full_text>, "label": <title>}.
    """
    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            data = json.loads(line)
            title = data.get("title", "")
            full_text = data.get("full_text", "").strip()
            if not title or not full_text:
                continue
            # one JSON object per line: text → label
            json.dump({"text": full_text, "label": title}, outfile)
            outfile.write("\n")
    print(f"Training data written to {output_path}")

def train_model(data_path, model_path):
    """
    Trains a simple TF-IDF + LogisticRegression model to predict page titles from page text.
    Saves the trained pipeline to `model_path`.
    """
    df = pd.read_json(data_path, lines=True)
    X = df["text"]
    y = df["label"]

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=3000, stop_words="english")),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)

    acc = pipe.score(X_test, y_test)
    print(f"Accuracy on held-out set: {acc:.4f}")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipe, model_path)
    print(f"Model saved to {model_path}")

def predict_question(model_path, question):
    """
    Loads a pretrained classifier and returns the predicted 'title' for a given question string.
    """
    model = joblib.load(model_path)
    return model.predict([question])[0]

if __name__ == "__main__":
    convert_to_training_data("../scrapy_project/output/combined_clean.jl", "flat_train.jsonl")
    train_model("flat_train.jsonl", "models/text_topic_model.pkl")
    print(predict_question("models/text_topic_model.pkl", "How can I do a corner jump?"))
