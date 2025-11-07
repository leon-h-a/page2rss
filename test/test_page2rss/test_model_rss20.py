import unittest
from page2rss.models.rss20 import RSSPage, RSSArticle

article_mandatory = "<item><title>some article</title><link /><description /><content:encoded>&lt;![CDATA[]]&gt;</content:encoded></item>"
article_full = "<item><title>another article</title><link>https://some.link.com</link><description>short description</description><content:encoded>&lt;![CDATA[]]&gt;</content:encoded><author>r, a, n, d, o, m</author><category>bla</category><pubDate>Wed, 07 Nov 2025 15:30:00 GMT</pubDate></item>"
page_mandatory = """<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0"
                 xmlns:content="http://purl.org/rss/1.0/modules/content/">
              <channel>
                <channel></channel>
              </channel>
        </rss>"""
page_full = """<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0"
                 xmlns:content="http://purl.org/rss/1.0/modules/content/">
              <channel>
                <channel></channel>
              </channel>
        </rss>"""
page_with_two_articles = """<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0"
                 xmlns:content="http://purl.org/rss/1.0/modules/content/">
              <channel>
                <channel><item><title>first article</title><link /><description /><content:encoded>&lt;![CDATA[]]&gt;</content:encoded></item><item><title>second article</title><link /><description /><content:encoded>&lt;![CDATA[]]&gt;</content:encoded></item></channel>
              </channel>
        </rss>"""


class TestRSS20Article(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_mandatory_article(self):
        article = RSSArticle(
            title="some article"
        )
        self.assertEqual(article.xml(), article_mandatory)

    def test_full_article(self):
        article = RSSArticle(
            title="another article",
            description="short description",
            link="https://some.link.com",
            author="random",
            category="bla",
            comments="nah",
            enclosure="nope",
            guid="1234",
            pubDate="Wed, 07 Nov 2025 15:30:00 GMT",
            source="bla",
        )
        self.assertEqual(article.xml(), article_full)

    @classmethod
    def tearDownClass(cls):
        pass


class TestRSS20Page(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_mandatory_page(self):
        page = RSSPage(
            title="some main page",
            link="some article",
            description="some article"
        )
        self.assertEqual(page.xml(), page_mandatory)

    def test_full_page(self):
        page = RSSPage(
            title="another main page",
            link="https://some.link.com",
            description="some desc",
            language="en",
            copyright="no",
            managingEditor="AE",
            webMaster="EA",
            pubDate="Wed, 07 Nov 2025 15:30:00 GMT",
            lastBuildDate="Wed, 07 Nov 2025 15:30:00 GMT",
            category="no",
            generator="some",
            docs="never",
            cloud="always",
            ttl="-1",
            image="no",
            rating="10",
            textInput="yes",
            skipHours="1",
            skipDays="2",
        )
        self.assertEqual(page.xml(), page_full)

    @classmethod
    def tearDownClass(cls):
        pass


class TestRSS20PageWithArticle(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_page_with_article(self):
        article1 = RSSArticle(
            title="first article"
        )
        article2 = RSSArticle(
            title="second article"
        )
        page = RSSPage(
            title="some main page",
            link="some article",
            description="some article",
            articles=[article1, article2]
        )
        self.assertEqual(page.xml(), page_with_two_articles)

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main()
