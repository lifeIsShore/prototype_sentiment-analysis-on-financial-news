import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# === Load Features ===
data_path = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\features\tfidf_features_labels.npz"
data = np.load(data_path)
X, y = data["X"], data["y"]

# === Split Dataset (Chronological or Random) ===
# chronological = True
chronological = False

if chronological:
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
else:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# === Train Logistic Regression ===
logreg = LogisticRegression(class_weight="balanced", max_iter=1000)
logreg.fit(X_train, y_train)
y_pred_logreg = logreg.predict(X_test)

# === Train XGBoost Classifier ===
xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)

# === Evaluation Function ===
def evaluate_model(y_true, y_pred, model_name):
    print(f"\nEvaluation for: {model_name}")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("F1 Score (macro):", f1_score(y_true, y_pred, average="macro"))
    print("F1 Score (class-wise):", f1_score(y_true, y_pred, average=None))
    print("\nClassification Report:\n", classification_report(y_true, y_pred))

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Bearish", "Neutral", "Bullish"], yticklabels=["Bearish", "Neutral", "Bullish"])
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.show()

    try:
        print("ROC AUC (macro):", roc_auc_score(y_true, model.predict_proba(X_test), multi_class="ovr", average="macro"))
    except:
        print("ROC AUC could not be calculated.")

# === Evaluate Both Models ===
evaluate_model(y_test, y_pred_logreg, "Logistic Regression")
evaluate_model(y_test, y_pred_xgb, "XGBoost Classifier")
