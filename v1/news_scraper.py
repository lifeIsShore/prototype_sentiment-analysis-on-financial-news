# news_scraper.py
# Description: Functions for scraping financial news headlines, primarily from Yahoo Finance,
# and saving the collected data.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

# Standard User-Agent to mimic a browser.
# Using a common browser User-Agent might sometimes help avoid blocks.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def scrape_yahoo_finance_for_ticker(ticker_symbol):
    """
    Scrapes news headlines for a given ticker symbol from Yahoo Finance.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL').

    Returns:
        list: A list of dictionaries, where each dictionary contains details of a news item
              (ticker, headline, url, source, scraped_timestamp, article_timestamp_raw).
              Returns an empty list if no news is found or an error occurs.
    """
    # !! IMPORTANT !!
    # VERIFY THIS URL MANUALLY IN A BROWSER. YAHOO FINANCE CHANGES FREQUENTLY.
    # If the previous run returned 404, this URL might be incorrect or the page structure changed significantly.
    # Based on your output, this URL is still returning 404. Find the correct one first!
    url = f"https://finance.yahoo.com/quote/{ticker_symbol}/news"
    news_items = []
    articles = [] # Initialize articles here to prevent UnboundLocalError

    print(f"\nScraping news for '{ticker_symbol}' from Yahoo Finance ({url})...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20) # Increased timeout slightly

        if response.status_code == 503:
            print(f"Yahoo Finance returned a 503 Service Unavailable for '{ticker_symbol}'. The server might be temporarily down or rate-limiting. Try again later.")
            return [] # Stop processing this ticker if 503 occurs

        response.raise_for_status()  # Raise an HTTPError for other bad responses (4XX or 5XX)

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Updated Selectors Based on Provided HTML Snippet ---
        # We are targeting the <li> elements that represent individual news stories.
        # The class 'stream-item story-item' seems more stable than the 'yf-' appended part.
        # Alternatively, could target <section data-testid="storyitem">
        articles = soup.find_all('li', class_=lambda x: x and 'stream-item story-item' in x)

        if not articles:
             # Fallback: Try finding by data-testid on the section element
            articles = soup.find_all('section', {'data-testid': 'storyitem'})
            if articles:
                 print(f"Found {len(articles)} potential article items using data-testid selector.")
            else:
                # Check for common "no news" messages or different page structures
                no_news_indicator = soup.find(text=lambda t: t and "There are no news reports for this period" in t)
                if no_news_indicator:
                    print(f"Yahoo Finance indicates no news available for '{ticker_symbol}'.")
                else:
                    # This message will print if we got a 200 OK but couldn't find articles
                    print(f"Could not find news articles container for '{ticker_symbol}' using known selectors. Page structure might have changed.")
                return []
        else:
             print(f"Found {len(articles)} potential article items using li class selector.")


        for article_container in articles:
            # Inside the container (either li or section):
            # Find the headline text within an <h3> tag that has class 'clamp'
            # Find the link URL from an <a> tag that has class 'titles' and an href attribute
            # Find the div containing source and timestamp, which has class 'publishing'

            headline_tag = article_container.find('h3', class_=lambda x: x and 'clamp' in x)
            link_tag = article_container.find('a', class_=lambda x: x and 'titles' in x, href=True) # Get the specific link for the headline
            meta_info_div = article_container.find('div', class_=lambda x: x and 'publishing' in x)


            if headline_tag and link_tag:
                title = headline_tag.get_text(strip=True)
                link = link_tag['href']

                # Ensure the link is absolute if it's relative
                if link and not link.startswith('http'):
                    link = f"https://finance.yahoo.com{link}"

                source_text = "N/A"
                article_timestamp_str = "N/A"

                # Extract source and timestamp from the meta info div
                if meta_info_div:
                    # The text is typically "Source • Time"
                    meta_text = meta_info_div.get_text(separator=' • ', strip=True) # Use ' • ' as separator for clean split
                    parts = [p.strip() for p in meta_text.split('•')]
                    if parts:
                        # Assume the part before the first '•' is the source
                        potential_source = parts[0]
                         # Basic check to avoid picking up non-source text if structure is weird
                        if len(potential_source) > 1 and len(potential_source) < 50 and not potential_source.lower().startswith("ad"):
                            source_text = potential_source

                        # Assume the part after the first '•' (if exists) is the time
                        if len(parts) > 1:
                            article_timestamp_str = parts[1]
                        # If only one part, maybe it's just the time (like "2 hours ago") or just the source
                        elif "ago" in meta_text or ":" in meta_text or "/" in meta_text or len(meta_text.split()) > 1:
                             # Heuristic: if it looks like a timestamp, keep it
                             article_timestamp_str = meta_text

                news_items.append({
                    'ticker': ticker_symbol,
                    'headline': title,
                    'url': link,
                    'source': source_text,
                    'scraped_timestamp': datetime.now().isoformat(),
                    'article_timestamp_raw': article_timestamp_str
                })

            time.sleep(0.05) # Add a small delay between processing articles

    except requests.exceptions.Timeout:
        print(f"Timeout occurred while trying to reach Yahoo Finance for '{ticker_symbol}'.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for '{ticker_symbol}': {http_err} (Status code: {response.status_code if 'response' in locals() else 'N/A'})")
        if 'response' in locals() and response.status_code == 404:
            print(f"'{ticker_symbol}' news page not found at the expected URL.")
        # Note: Script execution continues after printing the error message
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred while scraping '{ticker_symbol}' from Yahoo Finance: {req_err}")
        # Note: Script execution continues after printing the error message
    except Exception as e:
        print(f"An unexpected error occurred while scraping '{ticker_symbol}' from Yahoo Finance: {e}")
        # Note: Script execution continues after printing the error message

    # This final print block is outside the try...except and will always run.
    # articles is now always defined due to initialization.
    if news_items:
        print(f"Successfully extracted {len(news_items)} news items for '{ticker_symbol}'.")
    elif 'response' in locals() and response.status_code == 503:
         # 503 is a specific temporary error, the message is already printed inside the try block.
         pass # Do nothing more here
    else:
         # This covers cases where news_items is empty due to 404, other HTTP error,
         # other request errors, or selectors not finding any articles after a 200 OK.
         print(f"No news items successfully extracted for '{ticker_symbol}'. Check the URL and selectors if needed.")

    return news_items


def save_news_to_csv(all_news_data, filename="financial_news_headlines.csv"):
    """
    Saves a list of news data (dictionaries) to a CSV file.
    Args:
        all_news_data (list): A list of dictionaries, where each dictionary is a news item.
        filename (str): The name of the CSV file to save the data to.
    """
    if not all_news_data:
        print("No news data provided to save.")
        return

    try:
        df = pd.DataFrame(all_news_data)

        # Ensure all expected columns are present, add if missing
        expected_columns = [
            'ticker', 'headline', 'url', 'source',
            'article_timestamp_raw', 'scraped_timestamp'
        ]
        for col in expected_columns:
            if col not in df.columns:
                df[col] = "N/A" # Add missing column with default value

        df = df[expected_columns]

        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Data successfully saved to '{filename}'. Total articles: {len(df)}")
    except Exception as e:
        print(f"An error occurred while saving data to CSV '{filename}': {e}")

if __name__ == '__main__':
    print("Testing news_scraper.py...")
    # Use a ticker you have confirmed manually has news at the target URL
    # !! REMINDER: Manually verify https://finance.yahoo.com/quote/AAPL/news first !!
    sample_ticker = 'AAPL'
    aapl_news = scrape_yahoo_finance_for_ticker(sample_ticker)

    if aapl_news:
        print(f"\nSample news for {sample_ticker}:")
        # Print a few samples
        for i, item in enumerate(aapl_news[: min(5, len(aapl_news))]):
            print(f" {i+1}. Headline: {item.get('headline', 'N/A')}")
            print(f"    URL: {item.get('url', 'N/A')}")
            print(f"    Source: {item.get('source', 'N/A')}, Time: {item.get('article_timestamp_raw', 'N/A')}")
        save_news_to_csv(aapl_news, filename=f"{sample_ticker}_test_news.csv")
    else:
        print(f"No news found or extracted for {sample_ticker} during the test.")