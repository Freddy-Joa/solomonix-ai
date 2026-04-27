import joblib
import pandas as pd

# Load trained model and encoders
model = joblib.load("models/delay_model.pkl")
encoders = joblib.load("models/delay_encoders.pkl")


def predict_delay(
    case_type,
    pending_days,
    evidence_pages,
    witness_count,
    priority_level,
    judge_load
):
    """
    Predict case delay risk.
    """
    encoded_case_type = encoders["case_type"].transform([case_type])[0]
    encoded_priority = encoders["priority_level"].transform(
        [priority_level]
    )[0]

    input_data = pd.DataFrame([{
        "case_type": encoded_case_type,
        "pending_days": pending_days,
        "evidence_pages": evidence_pages,
        "witness_count": witness_count,
        "priority_level": encoded_priority,
        "judge_load": judge_load
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return prediction, probability