# evaluate.py
# Generates reports/metrics_summary.md and reports/confusion_matrix.png

import os
import sys
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# ---------- Paths  ----------
DATA_PATH = os.environ.get("DATA_PATH", "issues.csv")
# If your file is named differently, set DATA_PATH env var or change above.
# Model path based on your screenshot: app/model/<something>.joblib or .pkl
# We'll auto-pick the first *.joblib or *.pkl in app/model/
MODEL_DIR = "app/model"
REPORTS_DIR = "reports"

os.makedirs(REPORTS_DIR, exist_ok=True)

# ---------- Locate model file ----------
model_path = None
if os.path.isdir(MODEL_DIR):
    for fn in os.listdir(MODEL_DIR):
        if fn.endswith((".joblib", ".pkl")):
            model_path = os.path.join(MODEL_DIR, fn)
            break

if model_path is None:
    print(" Could not find a model file in app/model (.joblib or .pkl).")
    sys.exit(1)

print(f"🔎 Using model: {model_path}")

# ---------- Load data ----------
if not os.path.exists(DATA_PATH):
    print(f" Data file not found: {DATA_PATH}")
    sys.exit(1)

df = pd.read_csv(DATA_PATH)
print(f"📄 Loaded {len(df):,} rows from {DATA_PATH}")

# Try to infer text & label columns if user hasn’t set them explicitly
# COMMON TEXT COLUMNS
TEXT_CANDIDATES = [
    "text", "issue_text", "body", "description", "desc", "message", "content",
    "title_description", "title_desc", "title_body"
]
# COMMON LABEL COLUMNS
LABEL_CANDIDATES = ["label", "target", "is_bug", "bug", "class", "y"]

text_col = next((c for c in TEXT_CANDIDATES if c in df.columns), None)
label_col = next((c for c in LABEL_CANDIDATES if c in df.columns), None)


if text_col is None and "title" in df.columns and "description" in df.columns:
    text_col = "__combined_text__"
    df[text_col] = (df["title"].fillna("") + ". " + df["description"].fillna("")).str.strip()

if text_col is None:
    for c in df.columns:
        if df[c].dtype == "object":
            text_col = c
            break

if text_col is None or label_col is None:
    print(" Could not infer columns.")
    print("   Found columns:", list(df.columns))
    print("   Tips:")
    print("   - Text column should be one of:", TEXT_CANDIDATES, "or combine title+description.")
    print("   - Label column should be one of:", LABEL_CANDIDATES, "with values like 0/1.")
    sys.exit(1)

print(f" Using text column:  {text_col}")
print(f" Using label column: {label_col}")

X = df[text_col].fillna("").astype(str).tolist()
y_true = df[label_col].values
model = joblib.load(model_path)
y_pred = model.predict(X)

# ---------- Save classification metrics ----------
report_text = classification_report(y_true, y_pred, digits=3)
with open(os.path.join(REPORTS_DIR, "metrics_summary.md"), "w") as f:
    f.write("# Model Evaluation Metrics\n\n")
    f.write("```\n")
    f.write(report_text)
    f.write("\n```\n")
print(" Saved reports/metrics_summary.md")

# ---------- Save confusion matrix ----------
cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.title("Confusion Matrix")
plt.savefig(os.path.join(REPORTS_DIR, "confusion_matrix.png"), bbox_inches="tight")
plt.close()
print("Saved reports/confusion_matrix.png")

print("\n Done. Link these in your README:\n"
      " - reports/metrics_summary.md\n"
      " - reports/confusion_matrix.png\n")
