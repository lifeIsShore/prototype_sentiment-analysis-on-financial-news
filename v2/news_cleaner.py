# File: news_cleaner.py
import json
import re
import os
import nltk
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
nltk.download('stopwords')

# Define combined stopwords
english_stopwords = set(stopwords.words('english'))
finance_stopwords = {
    "stock", "market", "share", "shares", "trading", "trader", "stocks",
    "equity", "equities", "bond", "bonds", "portfolio", "investment",
    "investor", "finance", "financial", "capital", "returns", "index",
    "indices", "fund", "funds", "price", "valuation", "rate", "rates"
}
combined_stopwords = english_stopwords.union(finance_stopwords)

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove non-alphanumerics (but keep financial punctuation)
    text = re.sub(r"[^a-z0-9%\$.,\-\(\)\s]", " ", text)
    # Tokenize
    words = text.split()
    # Remove stopwords
    filtered_words = [word for word in words if word not in combined_stopwords]
    # Rejoin
    return " ".join(filtered_words)

def clean_news_file(ticker):
    input_path = os.path.join("v2", "input", f"{ticker}_news.json")
    output_path = os.path.join("v2", "input", f"{ticker}_news_cleaned.json")

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = []
    for entry in data:
        cleaned_data.append({
            "headline": clean_text(entry["headline"]),
            "text": clean_text(entry["text"])
        })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Cleaning complete. Output: {output_path}")
