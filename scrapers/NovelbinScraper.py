from scrapers.scraper_strategy_interface import ScraperStrategy
from ConnectionHandler import ConnectionHandler
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from ConnectionHandler import ConnectionHandler
import time

class NovelbinScraper(ScraperStrategy):
    def __init__(self):
        self.connection = ConnectionHandler(max_retries=5)
        self.log_class_name()

    def scrape(self, url):
        html = self.connection.connect(url)  # Returns HTML string
        soup = BeautifulSoup(html, "html.parser")

        # Extract title and chapter info
        novel_title_elem = soup.find(class_="novel-title")
        chapter_title_elem = soup.find(class_="chr-title")
        chapter_elem = soup.find(class_="chr-c")
        next_chapter_link_elem = soup.find(id="next_chap")

        if not (novel_title_elem and chapter_title_elem and chapter_elem):
            raise Exception(f"Required elements not found in HTML. {url}")
        
        novel_title = novel_title_elem.get("title", "").strip()
        chapter_title = chapter_title_elem.get("title", "").strip()


        # Clean chapter content
        for tag in chapter_elem.find_all(["script", "style"]):
            tag.decompose()

        for div in chapter_elem.find_all("div", class_="unlock-buttons text-center"):
            div.decompose()

        chapter_text = chapter_elem.get_text(separator="\n").strip()

        # Handle next chapter link
        is_disabled = next_chapter_link_elem.has_attr("disabled") if next_chapter_link_elem else True
        next_chapter_link = None if is_disabled else next_chapter_link_elem.get("href", None)

        return {
            "novel_title": novel_title,
            "chapter_title": chapter_title,
            "chapter_text": chapter_text,
            "next_chapter_link": next_chapter_link,
        }