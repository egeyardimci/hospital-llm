import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON file
file_path = "./results.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Group by test_id and calculate average evaluation_score (assuming it's numeric or defaulting to 0)
df['evaluation_score'] = df.get('evaluation_score', 0)
avg_scores = df.groupby("test_id")["evaluation_score"].mean().reset_index()

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(avg_scores["test_id"].astype(str), avg_scores["evaluation_score"])
plt.xlabel("Test ID")
plt.ylabel("Average Evaluation Score")
plt.title("Average Evaluation Score by Test")
plt.tight_layout()
plt.grid(axis='y')
plt.show()
