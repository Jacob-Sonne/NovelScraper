# NovelScraper

# How to run
Use the following command to run the script. The link has to have an associated scraper in the scraper factory and scraper folder.
```
python3 main.py <LINK_TO_WEBSITE>
```
Example:
```
python3 main.py https://novelbin.com/b/god-tier-farm/cchapter-1
```
Result:  
![image](https://github.com/user-attachments/assets/c3c2aa03-a63f-46b2-8a51-3b7fb278fb95)


# Adding more scrapers
1) Create a scraper inside the scrapers folder:
```
from scrapers.scraper_strategy_interface import ScraperStrategy
from bs4 import BeautifulSoup
from ConnectionHandler import ConnectionHandler

class NewScraper(ScraperStrategy):
    def __init__(self):
        self.connection = ConnectionHandler(max_retries=5)
        self.log_class_name()

    def scrape(self, url):
        html = self.connection.connect(url)  # Returns HTML string
        soup = BeautifulSoup(html, "html.parser")

        # scrape the parts of the HTML you want with BeautifulSoup
        # novel_title = soup.find("h1", class_="tit").find("a").get_text(strip=True)
        # ...

        return {
            "novel_title": novel_title,
            "chapter_title": chapter_title,
            "chapter_text": chapter_text,
            "next_chapter_link": next_chapter_link,
        }
```
2) Add the scraper to the scraper_factory file:
```
from scrapers.scraper_strategy_interface import ScraperStrategy
# Importing all the implemented scrapers:
from scrapers.NovelbinScraper import NovelbinScraper
from scrapers.FreewebnovelScraper import FreewebnovelScraper
from scrapers.NewScraper import NewScraper  # <--------- Import your scraper.

SCRAPER_REGISTRY = {
    "novelbin.com": NovelbinScraper,
    "freewebnovel.com": FreewebnovelScraper,
    "Newscraperwebsite.com": NewScraper,    # <--------- Add this line with the correct base link and name scraper name.
}
```
