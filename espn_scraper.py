from selenium import webdriver
from selenium.webdriver.common.by import By
import concurrent.futures

def process_url(url, idx):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        element = driver.find_element(By.CLASS_NAME, "PageLayout__Main")
        text = element.text
        with open(f"outputs/MatchSummary_{idx}.txt", "w", encoding="utf-8") as f:
            f.write(text)
    finally:
        driver.quit()

def self_scraper(urls):
    # Process all URLs concurrently and save output to separate files
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_url, url, idx) for idx, url in enumerate(urls)]
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    urls = ['https://www.espn.in/football/report/_/gameId/704766', 'https://www.espn.in/football/report/_/gameId/712534', 'https://www.espn.in/football/report/_/gameId/735156']
    self_scraper(urls)