import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the project tasks with task leaders
tasks = [
    ("Project Planning", "2025-03-10", "2025-06-24", "All Members", "Ege"),
    ("Data Inspection", "2025-03-25", "2025-05-30", "Emre", "Emre"),
    ("Question Answer Pair Generation", "2025-03-25", "2025-08-10", "Emre", "Emre"),
    ("Data Preprocessing", "2025-03-25", "2025-05-30", "Other Group Members"),
    ("VectorDB Creation", "2025-03-25", "2025-05-25", "Ege", "Ege"),
    ("Test Framework Development & Maintenance", "2025-03-25", "2025-08-10", "Ege, Suat", "Ege"),
    ("LLM & Embedding Model Testing", "2025-03-25", "2025-08-10", "Ege, Suat", "Suat"),
    ("Model Benchmarks & Evaluation", "2025-05-10", "2025-09-10", "Suat, Emre", "Suat"),
    ("Knowledge Graph Construction", "2025-03-25", "2025-09-10", "Other Group Members"),
    ("Query Mechanism Development", "2025-07-05", "2025-09-10", "All Members", "Emre"),
    ("Chatbot Interface Development", "2025-07-05", "2025-10-10", "All Members", "Ege"),
    ("System Integration & Testing", "2025-09-01", "2025-11-30", "All Members", "Ege"),
    ("Performance Optimization", "2025-10-15", "2025-12-15", "All Members", "Suat"),
    ("Final Testing & Validation", "2025-12-01", "2026-01-15", "All Members", "Ege"),
    ("Documentation & Report Writing", "2025-11-10", "2026-01-20", "All Members", "Suat"),
    ("Final Presentation & Submission", "2026-01-01", "2026-01-30", "All Members", "Emre"),
]

# Convert tasks to a DataFrame
df = pd.DataFrame(tasks, columns=["Task", "Start Date", "End Date", "Responsible", "Task Leader"])
df["Start Date"] = pd.to_datetime(df["Start Date"])
df["End Date"] = pd.to_datetime(df["End Date"])

# Rename columns for easier reference
df.rename(columns={"Start Date": "Start_Date", "End Date": "End_Date", "Task Leader": "Task_Leader"}, inplace=True)

# Create a Gantt chart with task leaders
fig, ax = plt.subplots(figsize=(14, 8))

# Plot tasks with overlapping timelines
for i, task in enumerate(df.itertuples(index=False)):
    ax.barh(task.Task, (task.End_Date - task.Start_Date).days, left=task.Start_Date, color="skyblue", edgecolor="black")
    ax.text(task.Start_Date, i, f"{task.Responsible} (Leader: {task.Task_Leader})", 
            va='center', ha='left', fontsize=10, color="black")

# Format chart
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_xlabel("Timeline")
ax.set_ylabel("Tasks")
ax.set_title("Project Schedule - Gantt Chart with Task Leaders (March 2025 - January 2026)")
plt.xticks(rotation=45)
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Show plot
plt.tight_layout()
plt.show()
