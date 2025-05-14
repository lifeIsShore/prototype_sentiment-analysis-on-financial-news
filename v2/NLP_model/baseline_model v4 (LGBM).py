from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# === Load features ===
data = np.load(r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\features\tfidf_features_labels.npz")
X, y = data["X"], data["y"]

# === Encode labels ===
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# === Train/test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42)

# === Train LightGBM with scikit-learn API ===
clf = LGBMClassifier(
    objective='multiclass',
    num_class=3,
    boosting_type='gbdt',
    n_estimators=1000,
    learning_rate=0.05,
    num_leaves=31,
    random_state=42
)

clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric='multi_logloss')

# === Predict & Evaluate ===
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("F1 Score (macro):", f1_score(y_test, y_pred, average='macro'))
print("F1 Score (class-wise):", f1_score(y_test, y_pred, average=None))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# === Confusion matrix ===
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, cmap='Blues', xticklabels=le.classes_, yticklabels=le.classes_)
plt.title("LightGBM - Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.show()

# === ROC AUC (macro) ===
try:
    print("ROC AUC (macro):", roc_auc_score(y_test, y_proba, multi_class="ovr", average="macro"))
except:
    print("ROC AUC could not be calculated.")
