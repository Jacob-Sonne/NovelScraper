from scrapers.scraper_strategy_interface import ScraperStrategy

class ScraperContext:
    def __init__(self, strategy: ScraperStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: ScraperStrategy):
        self.strategy = strategy

    def scrape(self, url: str) -> dict:
        return self.strategy.scrape(url)