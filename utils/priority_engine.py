# utils/priority_engine.py

def calculate_priority(pending_days, witnesses, evidence_pages):
    """
    Advanced judicial priority scoring.
    Produces realistic court-grade priority levels.
    """

    # Weighted Components
    days_score = min((pending_days / 1200) * 40, 40)
    witness_score = min((witnesses / 10) * 30, 30)
    evidence_score = min((evidence_pages / 500) * 30, 30)

    total_score = round(
        days_score +
        witness_score +
        evidence_score,
        2
    )

    # Priority Classification
    if total_score >= 85:
        level = "Critical"
    elif total_score >= 65:
        level = "High"
    elif total_score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return level, total_score