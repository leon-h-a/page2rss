import unittest
from pathlib import Path
from page2rss.scrape.scraper import Scraper
from page2rss.models.rss20 import RSSPage
from page2rss.xml.xml import XML 
from page2rss import TEST_ROOT 


class TestGithub(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = Scraper(data_dir=Path(""))
        cls.xm = XML()
        # get and store index.html via basic wget

    def test_github(self):
        path = str(TEST_ROOT / 'resources/github/index.html')

        bs = self.sc.index_load(page_path=path)

        articles = self.sc.article_get(
            bs=bs,
            tag="a",
            designator="Link--primary post-card__link"
        )
        self.assertEqual(21, len(articles))

        scraped_article = self.sc.article_scrape(articles[0])
        # todo: add some asserts

        # print(scraped_article.xml())

        asdf = RSSPage(
            title="asdf",
            link="",
            description="",
            articles=[scraped_article]
        )

        print(asdf.xml())


    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
