import pandas as pd
import tkinter as tk
from tkinter import ttk
import subprocess
import json
import os
import pickle
from news_cleaner import clean_news_file
from collections import Counter
import matplotlib.pyplot as plt

# === SETTINGS ===
CLEANSING_OUTPUT_DIR = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\model-in-action\cleansed-news"
MODEL_PATH = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\model-in-action\model\exported_model_logreg.pkl"
VECTORIZER_PATH = r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\model-in-action\model\tfidf_vectorizer.pkl"

# === Get the list of S&P 500 tickers ===
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers

# === Autocomplete Entry Widget ===
class AutocompleteEntry(ttk.Entry):
    def __init__(self, autocomplete_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_list = autocomplete_list
        self.var = self["textvariable"] = tk.StringVar()
        self.var.trace_add("write", self.changed)
        self.bind("<Right>", self.select_suggestion)
        self.listbox = None

    def changed(self, *args):
        value = self.var.get().upper()
        if value == "":
            self.hide_listbox()
            return

        matches = [s for s in self.autocomplete_list if s.startswith(value)]
        if matches:
            if not self.listbox:
                self.listbox = tk.Listbox(width=15)
                self.listbox.bind("<<ListboxSelect>>", self.on_select)
                self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
            self.listbox.delete(0, tk.END)
            for match in matches:
                self.listbox.insert(tk.END, match)
        else:
            self.hide_listbox()

    def on_select(self, event):
        if self.listbox:
            selection = self.listbox.get(self.listbox.curselection())
            self.var.set(selection)
            self.hide_listbox()

    def select_suggestion(self, event):
        if self.listbox and self.listbox.size() > 0:
            self.var.set(self.listbox.get(0))
            self.hide_listbox()

    def hide_listbox(self):
        if self.listbox:
            self.listbox.destroy()
            self.listbox = None

# === Run Scraper and Cleaner ===
def run_scraper(ticker):
    if ticker:
        print(f"[•] Running news scraper for {ticker}...")
        subprocess.run(["python", r"C:\Users\ahmty\Desktop\HFU\6 Sechstesemester\NLP\project\prototype\v2\model-in-action\news_scraper_input.py", ticker])
        print(f"[•] Cleaning scraped news for {ticker}...")
        clean_news_file(ticker, output_dir=CLEANSING_OUTPUT_DIR)
        print("[✓] Cleansing complete. Running prediction...")
        run_prediction()
    else:
        print("Please enter a ticker.")

# === Run Prediction and Show Results ===
def run_prediction():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)

    all_texts = []
    for filename in os.listdir(CLEANSING_OUTPUT_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(CLEANSING_OUTPUT_DIR, filename), encoding="utf-8") as f:
                news_items = json.load(f)
                all_texts += [item["text"] for item in news_items if "text" in item]

    if not all_texts:
        print("No news found for prediction.")
        return

    X = vectorizer.transform(all_texts)
    preds = model.predict(X)

    counts = Counter(preds)
    label_map = {0: "Bearish", 1: "Neutral", 2: "Bullish"}
    label_names = [label_map[i] for i in preds]

    # Pie chart
    labels = list(set(label_names))
    values = [label_names.count(l) for l in labels]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=["red", "green", "gray"], startangle=140)
    plt.title("Sentiment Distribution")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig("v2/model-in-action/sentiment_distribution.png")
    plt.show()

    # Insight
    total = sum(counts.values())
    bullish_ratio = counts.get(2, 0) / total
    bearish_ratio = counts.get(0, 0) / total

    print("\nInsight:")
    if bullish_ratio > 0.6:
        print("Sentiment is bullish — stock might increase.")
    elif bearish_ratio > 0.6:
        print("Sentiment is bearish — stock might decline.")
    else:
        print("Mixed or neutral sentiment — no dramatic change expected.")

# === GUI ===
def main():
    root = tk.Tk()
    root.title("Stock News Sentiment Analyzer")
    root.geometry("300x200")

    sp500_tickers = get_sp500_tickers()

    tk.Label(root, text="Enter Ticker Symbol:").pack(pady=10)
    entry = AutocompleteEntry(sp500_tickers, root)
    entry.pack()

    button = tk.Button(root, text="Analyze News", command=lambda: run_scraper(entry.get()))
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
