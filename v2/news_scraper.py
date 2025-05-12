from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Set up the Chrome driver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if headless is needed
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

def scrape_yahoo_finance(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/news/"
    driver.get(url)

    # Click the "Zum Ende" (scroll down) button if present
    try:
        scroll_down_button = driver.find_element(By.XPATH, '//button[@id="scroll-down-btn"]')
        scroll_down_button.click()
        print('Clicked "Zum Ende" button.')
    except Exception as e:
        print('Scroll down button not found or already clicked:', e)

    # Dismiss consent banner if present
    try:
        consent_button = driver.find_element(By.XPATH, '//button[@class="btn secondary reject-all" and text()="Alle ablehnen"]')
        consent_button.click()
        print("Consent banner dismissed.")
    except Exception as e:
        print("Consent banner not found or already dismissed:", e)

    # Wait for the specific news list to be present
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[2]/section/div/div/div/div/ul'))
        )
        print("News list loaded successfully.")
    except Exception as e:
        print("Failed to load news list:", e)
        driver.quit()
        return

    time.sleep(3)  # Let the content load fully

    # Scrape the news
    headlines = []
    scroll_attempts = 0
    max_scroll_attempts = 5

    while len(headlines) < 15 and scroll_attempts < max_scroll_attempts:  # Limit scroll attempts
        news_items = driver.find_elements(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[2]/section/div/div/div/div/ul/li')
        print(f"Found {len(news_items)} news items on this scroll attempt.")

        for item in news_items:
            if len(headlines) >= 15:
                break  # Stop if we have enough headlines

            try:
                headline = item.find_element(By.XPATH, './/h3').text
                text = item.find_element(By.XPATH, './/p').text
                headlines.append({"headline": headline, "text": text})
            except Exception as e:
                print("Error extracting headline or text:", e)

        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)
        scroll_attempts += 1
        time.sleep(5)

    # Save headlines to a JSON file
    output_file = f"{ticker}_news.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(headlines, f, ensure_ascii=False, indent=4)

    print(f"Saved {len(headlines)} headlines to {output_file}.")

# Example usage
scrape_yahoo_finance("AAPL")

# Close the driver
driver.quit()
