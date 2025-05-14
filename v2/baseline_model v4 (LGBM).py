import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# === Load Features ===
data_path = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\features\tfidf_features_labels.npz"
data = np.load(data_path)
X, y = data["X"], data["y"]

# === Encode labels (if necessary) ===
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# === Split Dataset (Random Split) ===
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42)

# === Train LightGBM Model ===
params = {
    'objective': 'multiclass',         # Multiclass classification
    'num_class': 3,                    # 3 classes: Bearish, Neutral, Bullish
    'metric': 'multi_logloss',         # Log loss metric for multiclass
    'boosting_type': 'gbdt',           # Gradient Boosting Decision Tree
    'num_leaves': 31,                  # Number of leaves in one tree
    'learning_rate': 0.05,             # Learning rate
    'feature_fraction': 0.9,           # Fraction of features to use for building each tree
    'bagging_fraction': 0.8,           # Fraction of samples used for building each tree
    'bagging_freq': 5,                 # Frequency of bagging
    'verbose': -1                      # Suppress LightGBM's output
}

lgb_train = lgb.Dataset(X_train, label=y_train)
lgb_test = lgb.Dataset(X_test, label=y_test, reference=lgb_train)

# Train the model
lgb_model = lgb.train(params, lgb_train, num_boost_round=1000, valid_sets=[lgb_train, lgb_test], early_stopping_rounds=50)

# === Predict and Evaluate ===
y_pred_lgb = lgb_model.predict(X_test, num_iteration=lgb_model.best_iteration)
y_pred_lgb_max = np.argmax(y_pred_lgb, axis=1)  # Get the class with the highest probability

# === Evaluation Function ===
def evaluate_model(model_name, y_true, y_pred, y_pred_proba):
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
        print("ROC AUC (macro):", roc_auc_score(y_true, y_pred_proba, multi_class="ovr", average="macro"))
    except:
        print("ROC AUC could not be calculated.")

# === Evaluate LightGBM ===
evaluate_model("LightGBM", y_test, y_pred_lgb_max, y_pred_lgb)

