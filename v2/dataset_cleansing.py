#that is a cleansing script for only the labeled data which labeled and exported as json from label-studio

import json
import os

def cleanse_and_concatenate(input_folder, output_file):
    cleaned_entries = []

    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(".json") and filename != os.path.basename(output_file):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    raw_data = json.load(f)
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON: {filename}")
                    continue

                for entry in raw_data:
                    try:
                        headline = entry["data"]["headline"]
                        text = entry["data"]["text"]
                        sentiment = entry["annotations"][0]["result"][0]["value"]["choices"][0]

                        cleaned_entries.append({
                            "headline": headline,
                            "text": text,
                            "sentiment": sentiment
                        })

                    except (KeyError, IndexError, TypeError):
                        continue  # Skip malformed entries

    with open(output_file, "w", encoding="utf-8") as out_f:
        json.dump(cleaned_entries, out_f, indent=2, ensure_ascii=False)

def remove_duplicates(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Invalid JSON file. Aborting deduplication.")
            return

    seen = set()
    unique_entries = []

    for item in data:
        key = (
            item.get("headline", "").strip().lower(),
            item.get("text", "").strip().lower(),
            item.get("sentiment", "").strip().lower()
        )

        if key not in seen:
            seen.add(key)
            unique_entries.append(item)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(unique_entries, f, indent=2, ensure_ascii=False)

# === CONFIGURATION ===
input_folder = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data"
output_folder = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\input\labeled_data\training_dataset"
output_file = os.path.join(output_folder, "training_dataset.json")

cleanse_and_concatenate(input_folder, output_file)
remove_duplicates(output_file)