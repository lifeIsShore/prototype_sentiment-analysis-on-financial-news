# File: news_cleaner.py
import json
import re
import os
import nltk
import spacy
from nltk.corpus import stopwords

# Download NLTK stopwords if not already available
nltk.download('stopwords')

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Define combined stopwords (English + financial domain)
english_stopwords = set(stopwords.words('english'))
finance_stopwords = {
    "stock", "market", "share", "shares", "trading", "trader", "stocks",
    "equity", "equities", "bond", "bonds", "portfolio", "investment",
    "investor", "finance", "financial", "capital", "returns", "index",
    "indices", "fund", "funds", "price", "valuation", "rate", "rates"
}
combined_stopwords = english_stopwords.union(finance_stopwords)

def clean_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove non-alphanumerics except finance-related symbols
    text = re.sub(r"[^a-z0-9%\$.,\-\(\)\s]", " ", text)

    # Tokenize and lemmatize
    doc = nlp(text)
    lemmatized_words = [
        token.lemma_ for token in doc
        if token.lemma_ not in combined_stopwords and not token.is_punct and not token.is_space
    ]

    # Join and normalize whitespace
    cleaned = " ".join(lemmatized_words)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned

def clean_news_file(ticker):
    input_path = os.path.join("v2", "input","cleansed-not_labeled", f"{ticker}_news.json")
    output_path = os.path.join("v2", "input","cleansed-not_labeled", f"{ticker}_news_cleaned.json")

    # Load raw news
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Clean headlines and texts
    cleaned_data = []
    for entry in data:
        cleaned_entry = {
            "headline": clean_text(entry.get("headline", "")),
            "text": clean_text(entry.get("text", ""))
        }
        cleaned_data.append(cleaned_entry)

    # Write cleaned data
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"[✓] Cleaning complete. Output: {output_path}")
