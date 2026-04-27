import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("data/legal_text_classification.csv")

# Keep only required columns
df = df[["case_text", "case_outcome"]].dropna()

# Features and Labels
X = df["case_text"]
y = df["case_outcome"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Build pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            max_features=50000,
            ngram_range=(1, 2),
            stop_words="english"
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            n_jobs=-1
        )
    )
])

# Train model
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy:.4f}\n")
print(classification_report(y_test, predictions))

# Save model
os.makedirs("models", exist_ok=True)

joblib.dump(
    model,
    "models/legal_classifier.pkl"
)

print("\n✅ Legal classifier saved successfully!")