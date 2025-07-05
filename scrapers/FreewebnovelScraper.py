from scrapers.scraper_strategy_interface import ScraperStrategy
from bs4 import BeautifulSoup
from ConnectionHandler import ConnectionHandler

class FreewebnovelScraper(ScraperStrategy):
    def __init__(self):
        self.connection = ConnectionHandler(max_retries=5)
        self.log_class_name()


    def scrape(self, url):
        html = self.connection.connect(url)  # Returns HTML string
        soup = BeautifulSoup(html, "html.parser")

        # Extract title and chapter info
        novel_title = soup.find("h1", class_="tit").find("a").get_text(strip=True)
        chapter_title = soup.find("span", class_="chapter").get_text(strip=True)
        chapter_elem = soup.find("div", id="article")
        next_chapter_link_elem = soup.find("a", title="Read Next chapter")

        if not (novel_title and chapter_title and chapter_elem):
            raise Exception(f"Required elements not found in HTML. {url}")
        
        # Clean chapter content
        for tag in chapter_elem.find_all(["script", "style"]):
            tag.decompose()

        for div in chapter_elem.find_all("div", style=True):
            div.decompose()

        empty_tags = [tag for tag in chapter_elem.find_all(["p", "h4"]) if not tag.get_text(strip=True)]
        for tag in empty_tags:
            tag.decompose()

        

        chapter_text = chapter_elem.get_text(separator="\n").strip()

        # Handle next chapter link
        next_chapter_link = None if not next_chapter_link_elem else "https://freewebnovel.com"+next_chapter_link_elem.get("href", None)

        return {
            "novel_title": novel_title,
            "chapter_title": chapter_title,
            "chapter_text": chapter_text,
            "next_chapter_link": next_chapter_link,
        }