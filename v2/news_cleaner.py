# File: news_cleaner.py
import json
import re
import os

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9%\$.,\-\(\)\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_news_file(ticker):
    input_path = os.path.join("v2\\input", f"{ticker}_news.json")
    output_path = os.path.join("v2\\input", f"{ticker}_news_cleaned.json")

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
