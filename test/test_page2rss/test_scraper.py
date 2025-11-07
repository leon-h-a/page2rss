import unittest
from pathlib import Path
from page2rss.scrape.scraper import Scraper
from page2rss.models.rss20 import RSSPage
from page2rss import TEST_ROOT 


class TestScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = Scraper(data_dir=Path(""))

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
