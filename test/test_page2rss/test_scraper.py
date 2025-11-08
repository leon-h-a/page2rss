import unittest
from page2rss.scrape.scraper import Scraper
from page2rss import TEST_INPUT_DIR, TEST_OUTPUT_DIR 


class TestScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sc = Scraper(
            input_dir=TEST_INPUT_DIR,
            output_dir=TEST_OUTPUT_DIR
        )

    def test_load_page_list(self):
        pages = self.sc.load_page_list()
        self.assertEqual(pages, [TEST_INPUT_DIR / "news.html"])

    def test_index_load(self):
        page = self.sc.index_load(TEST_INPUT_DIR / "news.html")
        self.assertTrue("<!DOCTYPE html>" in str(page))

    def test_article_get(self):
        page = self.sc.index_load(TEST_INPUT_DIR / "news.html")
        hrefs = self.sc.article_get(page, tag="a", designator="article-link")
        self.assertEqual(
            hrefs,
            [
                '../resources/page1.html',
                '../resources/page2.html',
                '../resources/page3.html',
                '../resources/page4.html'
            ]
        )

    def test_page_scrape(self):
        page = self.sc.page_scrape(
            ref=str(TEST_INPUT_DIR / "news.html"),
            local_file=True
        )
        self.assertEqual(page.title, "Latest Articles")
        self.assertEqual(page.language, "en")
        self.assertEqual(page.articles, [])

    def test_article_scrape(self):
        article = self.sc.article_scrape(
            ref=str(TEST_INPUT_DIR / "../resources/page1.html"),
            local_file=True
        )
        self.assertEqual(
            article.title,
            "The Future of Artificial Intelligence in Software Development"
        )
        self.assertEqual(
            article.pubDate,
            "Fri, 07 Nov 2025 15:30:00 +0000"
        )

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main()
