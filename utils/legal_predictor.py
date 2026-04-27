import joblib

# Load trained legal classifier
model = joblib.load("models/legal_classifier.pkl")


def predict_case_outcome(case_text):
    """
    Predict legal outcome from case text.
    """
    prediction = model.predict([case_text])[0]
    probabilities = model.predict_proba([case_text])[0]
    confidence = max(probabilities)

    return prediction, confidence