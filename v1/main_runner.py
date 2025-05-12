# main_runner.py
# Description: Main script to orchestrate the financial news scraping process.
# Handles user input for ticker symbols and calls functions from other modules.

import time
import os # Added os module to check current working directory
from datetime import datetime

# --- Attempt to import from other modules ---
try:
    from sp500_utils import get_sp500_tickers
    from news_scraper import scrape_yahoo_finance_for_ticker, save_news_to_csv
    print("Successfully imported modules: sp500_utils, news_scraper")
except ImportError as e:
    print(f"ImportError occurred: {e}")
    print(f"Current working directory: {os.getcwd()}")
    print("Please ensure 'sp500_utils.py' and 'news_scraper.py' are in the same directory as 'main_runner.py'.")
    exit() # Exit if imports fail

# Configuration
# Time delay between scraping different tickers (in seconds) to be respectful to servers.
DELAY_BETWEEN_TICKERS = 5  # Increased delay

def get_user_ticker_choices():
    """
    Prompts the user to enter ticker symbols or choose from predefined options.

    Returns:
        list: A list of ticker symbols to scrape. Returns an empty list if input is invalid or user quits.
    """
    tickers_to_scrape = []
    while True:
        print("\nHow would you like to specify the S&P 500 companies (tickers) to scrape news for?")
        print("1. Enter ticker symbols manually (comma-separated, e.g., AAPL,MSFT,GOOGL)")
        print("2. Scrape for a predefined list of 'big shot' tickers (e.g., top tech)")
        print("3. Scrape for ALL S&P 500 companies (WARNING: This will take a very long time!)")
        print("4. Scrape for the first N S&P 500 companies (e.g., top 10 by current Wikipedia order)")
        print("Q. Quit")
        
        choice = input("Enter your choice (1-4 or Q): ").strip().upper()

        if choice == '1':
            user_input = input("Enter ticker symbols (comma-separated): ").strip().upper()
            if not user_input:
                print("No tickers entered. Please try again.")
                continue
            tickers_to_scrape = [ticker.strip() for ticker in user_input.split(',')]
            tickers_to_scrape = [t for t in tickers_to_scrape if t] 
            if not tickers_to_scrape:
                print("Invalid ticker format. Please ensure tickers are comma-separated and not empty.")
                continue
            print(f"Selected tickers for scraping: {tickers_to_scrape}")
            return tickers_to_scrape
        
        elif choice == '2':
            predefined_big_shots = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA', 'META', 'BRK-B', 'JPM', 'V']
            print(f"Using predefined 'big shot' tickers: {predefined_big_shots}")
            return predefined_big_shots
            
        elif choice == '3':
            confirm = input("Are you sure you want to scrape for all S&P 500 companies? (yes/no): ").strip().lower()
            if confirm == 'yes':
                all_sp500 = get_sp500_tickers() # This function is from sp500_utils
                if all_sp500:
                    print(f"Selected all {len(all_sp500)} S&P 500 tickers for scraping.")
                    return all_sp500
                else:
                    print("Could not retrieve the list of S&P 500 tickers. Please try another option.")
                    continue
            else:
                print("Scraping for all S&P 500 companies cancelled.")
                continue
        
        elif choice == '4':
            try:
                num_tickers = int(input("Enter the number of top S&P 500 companies to scrape (e.g., 10): ").strip())
                if num_tickers <= 0:
                    print("Please enter a positive number.")
                    continue
                all_sp500 = get_sp500_tickers() # This function is from sp500_utils
                if all_sp500:
                    tickers_to_scrape = all_sp500[:num_tickers]
                    print(f"Selected the first {len(tickers_to_scrape)} S&P 500 tickers: {tickers_to_scrape}")
                    return tickers_to_scrape
                else:
                    print("Could not retrieve the list of S&P 500 tickers. Please try another option.")
                    continue
            except ValueError:
                print("Invalid number. Please enter an integer.")
                continue

        elif choice == 'Q':
            print("Exiting ticker selection.")
            return []
            
        else:
            print("Invalid choice. Please enter a number between 1 and 4, or Q to quit.")

def run_news_pipeline():
    """
    Main function to run the news scraping pipeline.
    """
    print("--- NLP-Driven News Sentiment Analysis: Data Collection ---")
    print(f"Current working directory for main_runner.py: {os.getcwd()}") # Helps debug path issues
    
    target_tickers = get_user_ticker_choices()

    if not target_tickers:
        print("No tickers selected. Exiting program.")
        return

    all_news_collected = []
    start_time_pipeline = time.time()

    print(f"\nStarting news scraping for {len(target_tickers)} ticker(s): {', '.join(target_tickers)}")

    for i, ticker in enumerate(target_tickers):
        print(f"\n--- Processing Ticker {i+1}/{len(target_tickers)}: {ticker} ---")
        
        yahoo_news = scrape_yahoo_finance_for_ticker(ticker) # This function is from news_scraper
        if yahoo_news:
            all_news_collected.extend(yahoo_news)
        
        if i < len(target_tickers) - 1: 
            print(f"Waiting for {DELAY_BETWEEN_TICKERS} seconds before next ticker...")
            time.sleep(DELAY_BETWEEN_TICKERS)

    end_time_pipeline = time.time()
    pipeline_duration = end_time_pipeline - start_time_pipeline

    if all_news_collected:
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"financial_news_{timestamp_str}.csv"
        
        save_news_to_csv(all_news_collected, filename=output_filename) # This function is from news_scraper
    else:
        print("\nNo news was collected from any source for the selected tickers.")

    print(f"\n--- Pipeline Finished ---")
    print(f"Total tickers processed: {len(target_tickers)}")
    print(f"Total articles collected: {len(all_news_collected)}")
    print(f"Total pipeline duration: {pipeline_duration:.2f} seconds.")

if __name__ == '__main__':
    run_news_pipeline()
