# Stock News Sentiment Analyzer

This project analyzes the sentiment of stock-related news articles to help investors understand market trends. It scrapes the latest news for a given S&P 500 ticker, cleans and processes the text data, predicts sentiment using a pre-trained machine learning model, and visualizes the results.

## Features

- **News Scraper:** Automatically fetches recent news headlines and articles from Yahoo Finance for any S&P 500 stock ticker.
- **Text Cleaning:** Applies natural language processing techniques to remove noise and irrelevant words, improving prediction accuracy.
- **Sentiment Prediction:** Uses a logistic regression model with TF-IDF vectorization to classify news as Bullish, Neutral, or Bearish.
- **Interactive GUI:** Allows users to input ticker symbols with autocomplete support and view sentiment distribution through pie charts.
- **Insight Generation:** Provides a simple summary of overall market sentiment based on news data.

## How It Works

1. Enter a stock ticker symbol in the GUI.
2. The program scrapes news articles related to the ticker.
3. The news content is cleaned and preprocessed.
4. The cleaned text is transformed using a TF-IDF vectorizer.
5. A logistic regression model predicts the sentiment for each article.
6. Sentiment distribution is displayed visually, and a brief insight message is printed.

## Requirements

- Python 3.7+
- Libraries: pandas, tkinter, scikit-learn, spacy, nltk, matplotlib, selenium, requests
- SpaCy English model (`en_core_web_sm`) and NLTK stopwords downloaded
- ChromeDriver for Selenium (matching your Chrome version)

## Setup Steps

1. **Download and configure ChromeDriver for Selenium**

   - Download the ChromeDriver that matches your installed Chrome browser version from the [official site](https://sites.google.com/chromium.org/driver/).
   - Place the executable in a directory included in your system PATH, or specify its path in the scraper configuration.

2. **Place pre-trained model and vectorizer**

   - Copy `exported_model_logreg.pkl` and `tfidf_vectorizer.pkl` into the `model/` directory in the project root.

3. **Run the main GUI script**

   - Execute `main.py` to launch the application and start analyzing stock news sentiment.

---

## Project Structure

- `main.py`  
  The main graphical user interface and orchestrates the processes of scraping, cleaning, prediction, and visualization.

- `news_cleaner.py`  
  Contains functions responsible for cleaning and preprocessing the raw news text data.

- `news_scraper_input.py`  
  Uses Selenium to scrape the latest news articles for a given stock ticker.

- `model/`  
  Directory holding the serialized machine learning model and TF-IDF vectorizer.

- `cleansed-news/`  
  Stores JSON files containing cleaned news data after preprocessing.

- `charts/`  
  Contains generated pie charts visualizing sentiment distribution.

---

## Notes on Sentiment Labels

- **Bullish:** Indicates a positive market outlook based on news sentiment.

- **Neutral:** Suggests mixed or uncertain market signals.

- **Bearish:** Reflects a negative sentiment toward the stock.

---

## Disclaimer

The sentiment predictions are based solely on textual analysis of news articles and may not always correlate with actual stock price movements. This tool is designed for educational and informational use only and should not be considered financial advice.
