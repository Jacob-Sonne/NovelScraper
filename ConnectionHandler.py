from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import time

class ConnectionHandler:
    def __init__(self, max_retries = 5, backoff_factor=1):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    def connect(self, url):
        retries = 0
        while retries < self.max_retries:
            driver = webdriver.Chrome(options=self.options)
            try:
                driver.get(url)

                time.sleep(0.1)

                WebDriverWait(driver, 15).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )

                html = driver.page_source

                # Somehow detect if it is cloudflare or not:
                if self._is_cloudflare_challenge(html):
                    raise Exception("Cloudflare challenge detected")

                return html
            except Exception as e:
                retries += 1
                print(f"Connection attempt {retries} failed: {e}")
                driver.quit()
                wait = self.backoff_factor * (2 ** retries)
                time.sleep(wait)

        raise Exception(f"Failed to connect and load the page after {self.max_retries} attempts.")

    def _is_cloudflare_challenge(self, html: str) -> bool:
        html_lower = html.lower()
        #self.save_html_failure(html_lower)
        return ("verify you are human" in html_lower or "verifying you are human" in html_lower)


    def save_html_failure(self, html: str):
        filename = "html_failure.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Saved failure HTML to: {filename}")