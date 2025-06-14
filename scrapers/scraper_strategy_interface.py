from abc import ABC, abstractmethod

class ScraperStrategy(ABC):
    def log_class_name(self):
        print(self.__class__.__name__)

    @abstractmethod
    def scrape(self, url: str) -> dict:
        """
            Scrape data from a URL and return it as a dictionary
            Should have a novel title, chapter title and chapter contents.
        """
        pass