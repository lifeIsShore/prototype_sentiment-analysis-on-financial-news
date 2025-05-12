import pandas as pd
import tkinter as tk
from tkinter import ttk
import subprocess
from news_cleaner import clean_news_file



# Function to get the list of S&P 500 tickers
def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers

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

def run_scraper(ticker):
    if ticker:
        print(f"[•] Running news scraper for {ticker}...")
        subprocess.run(["python", "v2\\news_scraper_input.py", ticker])
        print(f"[•] Cleaning scraped news for {ticker}...")
        clean_news_file(ticker)
    else:
        print("Please enter a ticker.")


def main():
    root = tk.Tk()
    root.title("Stock News Scraper")
    root.geometry("300x200")

    # Get S&P 500 tickers and set it as the autocomplete list
    sp500_tickers = get_sp500_tickers()

    tk.Label(root, text="Enter Ticker Symbol:").pack(pady=10)

    # Create an autocomplete entry using the list of S&P 500 tickers
    entry = AutocompleteEntry(sp500_tickers, root)
    entry.pack()

    # Button to fetch news for the entered ticker
    button = tk.Button(root, text="Fetch News", command=lambda: run_scraper(entry.get()))
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
