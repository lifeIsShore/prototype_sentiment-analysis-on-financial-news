# tf idf + bert
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer

# === Load Dataset ===
json_path = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\training_dataset\training_dataset.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = [item["text"] for item in data]
labels = [item["sentiment"] for item in data]

# === Encode Labels ===
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# === TF-IDF Features ===
tfidf = TfidfVectorizer(max_features=5000)
X_tfidf = tfidf.fit_transform(texts).toarray()

# === BERT Embeddings (Sentence-BERT) ===
model_bert = SentenceTransformer("all-MiniLM-L6-v2")
X_bert = model_bert.encode(texts)

# === Combine TF-IDF and BERT ===
X_combined = np.hstack((X_tfidf, X_bert))

# === Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, stratify=y, random_state=42)

# === Train Models ===
logreg = LogisticRegression(class_weight="balanced", max_iter=1000)
logreg.fit(X_train, y_train)
y_pred_logreg = logreg.predict(X_test)

xgb = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)

# === Evaluation Function ===
def evaluate_model(model, X_test, y_true, y_pred, model_name):
    print(f"\nEvaluation for: {model_name}")
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("F1 Score (macro):", f1_score(y_true, y_pred, average="macro"))
    print("F1 Score (class-wise):", f1_score(y_true, y_pred, average=None))
    print("\nClassification Report:\n", classification_report(y_true, y_pred, target_names=label_encoder.classes_))

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.show()

    try:
        print("ROC AUC (macro):", roc_auc_score(y_true, model.predict_proba(X_test), multi_class="ovr", average="macro"))
    except Exception as e:
        print("ROC AUC could not be calculated:", str(e))

# === Evaluate ===
evaluate_model(logreg, X_test, y_test, y_pred_logreg, "Logistic Regression (TF-IDF + BERT)")
evaluate_model(xgb, X_test, y_test, y_pred_xgb, "XGBoost Classifier (TF-IDF + BERT)")

