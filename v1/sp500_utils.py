# sp500_utils.py
# Description: Utility functions related to the S&P 500 index,
# primarily for fetching the list of constituent tickers.

import pandas as pd

# URL for the Wikipedia page listing S&P 500 companies
SP500_WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

def get_sp500_tickers():
    """
    Retrieves the list of S&P 500 ticker symbols from Wikipedia.

    Returns:
        list: A list of ticker symbols (e.g., ['AAPL', 'MSFT', ...]).
              Returns an empty list if an error occurs.
    """
    print(f"Attempting to fetch S&P 500 tickers from: {SP500_WIKIPEDIA_URL}")
    try:
        # pandas.read_html() reads HTML tables into a list of DataFrame objects.
        # We expect the first table ([0]) on the Wikipedia page to be the S&P 500 constituents.
        table = pd.read_html(SP500_WIKIPEDIA_URL)[0]
        
        # The 'Symbol' column in the table contains the ticker symbols.
        # We convert this column to a Python list.
        tickers = table['Symbol'].tolist()
        
        # Clean up tickers: Some tickers from Wikipedia might have suffixes (e.g., "BRK.B" vs "BRK-B").
        # Yahoo Finance typically uses "-" for class distinctions.
        tickers = [ticker.replace('.', '-') for ticker in tickers]

        print(f"Successfully retrieved {len(tickers)} S&P 500 tickers.")
        return tickers
    except ImportError:
        print("Error: pandas library not found. Please ensure it's installed ('pip install pandas').")
        return []
    except KeyError:
        print("Error: Could not find the 'Symbol' column in the Wikipedia table. The page structure might have changed.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while fetching S&P 500 tickers: {e}")
        return []

if __name__ == '__main__':
    # Example usage of the function when this script is run directly.
    print("Testing get_sp500_tickers function from sp500_utils.py...")
    all_tickers = get_sp500_tickers()
    if all_tickers:
        print(f"First 10 tickers: {all_tickers[:10]}")
        print(f"Last 5 tickers: {all_tickers[-5:]}")
    else:
        print("Failed to retrieve S&P 500 tickers during test.")
