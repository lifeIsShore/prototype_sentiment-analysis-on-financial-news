import json

def extract_clean_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    clean_data = []

    for entry in raw_data:
        try:
            headline = entry["data"]["headline"]
            text = entry["data"]["text"]
            sentiment = entry["annotations"][0]["result"][0]["value"]["choices"][0]

            clean_entry = {
                "headline": headline,
                "text": text,
                "sentiment": sentiment
            }

            clean_data.append(clean_entry)
        except (KeyError, IndexError):
            continue  # Skip malformed entries

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=2)

# Example usage:
extract_clean_data("raw_input.json", "clean_output.json")
