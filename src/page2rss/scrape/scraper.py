from pathlib import Path
from bs4 import BeautifulSoup
from newspaper import Article
from email.utils import format_datetime
from page2rss import DATA_DIR
from page2rss.scrape import logger
from page2rss.models.models import RSSArticle

from readability import Document

import nltk
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


class Scraper:
    def __init__(self,
            data_dir: Path = DATA_DIR,
            use_nlp: bool = True
        ):
        self.data_dir = data_dir
        self.supported_tags = ["a"]
        self.use_nlp = use_nlp

    def load_page_list(self):
        pass

    def index_get(self, url: str):
        # wget
        pass

    def index_load(self, page_path: str) -> BeautifulSoup:
        logger.info(f"load {page_path}")
        with open(page_path, 'r') as index:
            return BeautifulSoup(index.read(), "html.parser")

    def article_get(self, bs: BeautifulSoup, tag: str, designator: str) -> list[str]:
        """
        tag: str            html element (div/article/a)
        designator: str     css identificator of said element
        """
        if tag not in self.supported_tags:
            raise ValueError(f"tag '{tag}' not supported")

        logger.info(f"find all <{tag}> with '{designator}' designator")
        hits = bs.find_all(tag, designator) # type: ignore
        return [hit["href"] for hit in hits] # type: ignore

    def article_scrape(self, href: str) -> RSSArticle:
        logger.info(f"scrape: {href}")
        # make this async (?)

        article = Article(href)
        article.download()
        article.parse()
        if self.use_nlp:
            logger.info("using nlp")
            article.nlp()

        doc = Document(article.html)
        clean_html = doc.summary()

        rss_article = RSSArticle(
            title=article.title,
            description=article.summary,
            content=clean_html,
            top_image=article.top_image,
            link=href,
            author=article.authors,
            pubDate=format_datetime(article.publish_date)
        )

        return rss_article 

    def run(self):
        pass

    def teardown(self):
        pass


if __name__ == "__main__":
    pass
