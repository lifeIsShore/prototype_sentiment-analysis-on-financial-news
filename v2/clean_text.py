import json
import re

# Load your input JSON data
with open('input.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_text(text):
    # Lowercase
    text = text.lower()

    # Remove all non-alphanumeric characters except finance-relevant ones
    text = re.sub(r"[^a-z0-9%\$.,\-\(\)\s]", " ", text)

    # Replace multiple whitespace with single space
    text = re.sub(r"\s+", " ", text)

    # Strip leading/trailing whitespace
    return text.strip()

# Clean headlines and texts
cleaned_data = []
for entry in data:
    cleaned_entry = {
        "headline": clean_text(entry["headline"]),
        "text": clean_text(entry["text"])
    }
    cleaned_data.append(cleaned_entry)

# Save the cleaned data
with open('cleaned_output.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

print("Cleaning complete. Output saved to 'cleaned_output.json'.")
