import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("data/court_delay_data.csv")

# Encode categorical columns
categorical_columns = ["case_type", "priority_level"]
encoders = {}

for column in categorical_columns:
    encoder = LabelEncoder()
    df[column] = encoder.fit_transform(df[column])
    encoders[column] = encoder

# Features and target
X = df.drop("delay_risk", axis=1)
y = df["delay_risk"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Model
model = XGBClassifier(
    n_estimators=300,
    max_depth=7,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="logloss"
)

# Train
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"\nModel Accuracy: {accuracy:.4f}\n")
print(classification_report(y_test, predictions))

# Save models
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/delay_model.pkl")
joblib.dump(encoders, "models/delay_encoders.pkl")

print("\n✅ Delay prediction model saved successfully!")