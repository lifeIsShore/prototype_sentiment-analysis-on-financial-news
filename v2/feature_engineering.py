import json
import os
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# === PATHS ===
input_path = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\training_dataset\training_dataset.json"
output_dir = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\features"
os.makedirs(output_dir, exist_ok=True)

# === Load JSON ===
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

texts = []
labels = []

label_map = {"Bearish": 0, "Neutral": 1, "Bullish": 2}

for item in data:
    combined_text = item["headline"] + " " + item["text"]
    texts.append(combined_text)
    labels.append(label_map[item["sentiment"]])

# === TF-IDF Vectorization ===
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))  # You can tweak max_features
X = vectorizer.fit_transform(texts)

# === Label Encoding ===
y = np.array(labels)

# === Save Features and Labels ===
np.savez_compressed(os.path.join(output_dir, "tfidf_features_labels.npz"), X=X.toarray(), y=y)

# Save vectorizer for future use
with open(os.path.join(output_dir, "tfidf_vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print("Feature engineering complete.")
print(f"Features shape: {X.shape}")
print(f"Labels shape: {y.shape}")
