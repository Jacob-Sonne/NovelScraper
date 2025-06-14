from scrapers.scraper_strategy_interface import ScraperStrategy
# Importing all the implemented scrapers:
from scrapers.NovelbinScraper import NovelbinScraper
from scrapers.FreewebnovelScraper import FreewebnovelScraper


SCRAPER_REGISTRY = {
    "novelbin.com": NovelbinScraper,
    "freewebnovel.com": FreewebnovelScraper,
}

def get_scraper_for_url(url: str) -> ScraperStrategy:
    for domain, ScraperClass in SCRAPER_REGISTRY.items():
        if domain in url:
            return ScraperClass()
    raise ValueError(f"No scraper found for URL: {url}")