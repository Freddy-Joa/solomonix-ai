import pandas as pd
import numpy as np

np.random.seed(42)

n_samples = 10000

case_types = [
    "Civil",
    "Criminal",
    "Family",
    "Corporate",
    "Property",
    "Tax"
]

priority_levels = [
    "Low",
    "Medium",
    "High",
    "Critical"
]

data = {
    "case_type": np.random.choice(case_types, n_samples),
    "pending_days": np.random.randint(30, 3000, n_samples),
    "evidence_pages": np.random.randint(20, 5000, n_samples),
    "witness_count": np.random.randint(1, 50, n_samples),
    "priority_level": np.random.choice(priority_levels, n_samples),
    "judge_load": np.random.randint(10, 120, n_samples)
}

df = pd.DataFrame(data)

# Smart target generation
delay_score = (
    (df["pending_days"] * 0.35) +
    (df["evidence_pages"] * 0.15) +
    (df["witness_count"] * 8) +
    (df["judge_load"] * 10)
)

df["delay_risk"] = (delay_score > 3500).astype(int)

df.to_csv("data/court_delay_data.csv", index=False)

print("✅ Dataset created successfully!")
print(f"Rows: {len(df)}")
print("Saved to: data/court_delay_data.csv")