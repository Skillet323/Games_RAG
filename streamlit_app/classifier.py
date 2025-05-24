import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

def load_data(filepath):
    return pd.read_json(filepath, lines=True)

def train_model(data_path, model_path):
    df = load_data(data_path)
    df['text'] = df['full_text']
    df['label'] = df['categories'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
    df = df[df['label'].notnull()]
    X = df['text']
    y = df['label']
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_train, y_train)
    acc = pipe.score(X_test, y_test)
    print(f"Accuracy: {acc:.4f}")
    joblib.dump(pipe, model_path)

def predict_topic(model_path, question):
    model = joblib.load(model_path)
    return model.predict([question])[0]

if __name__ == "__main__":
    train_model("../scrapy_project/output/celeste_pages2.jl", "../models/topic_classifier.pkl")
