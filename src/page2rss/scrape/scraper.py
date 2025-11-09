import time
import requests
from pathlib import Path
from configparser import ConfigParser
from bs4 import BeautifulSoup
from newspaper import Article
from page2rss.filesystem.operators import page_def_list
from readability import Document
from email.utils import format_datetime
from page2rss.models.rss20 import RSSArticle, RSSPage
from page2rss import CONFIG, INPUT_DIR, OUTPUT_DIR
from page2rss.filesystem.operators import (
    page_def_list,
    page_def_read,
    xml_page_save
)
from page2rss.scrape import logger

import nltk
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")


class Scraper:
    def __init__(
            self,
            input_dir: Path = INPUT_DIR,
            output_dir: Path = OUTPUT_DIR,
            use_nlp: bool = True
        ):
        """
        input:              points to dir where <index>.html pages are listed
        output:             points to dir where scraped .xml files are stored
        """
        self.input_dir = input_dir 
        self.output_dir = output_dir
        self.use_nlp = use_nlp

        parser = ConfigParser()
        parser.read(CONFIG)
        self.cfg = parser["scrape"]
        self.article_limit = int(self.cfg.get("article_limit", "3"))
        self.scrape_period = int(self.cfg.get("scrape_period", "0"))

    def run(self):
        while True:
            nicks = page_def_list()
            for nick in nicks:
                page_def = page_def_read(nick)
                if page_def:
                    page = self.page_scrape(ref=page_def.url)
                    index = self.index_load(ref=page_def.url)
                    articles = self.article_get(
                        bs=index,
                        tag=page_def.tag,
                        designator=page_def.css
                    )
                    scraped: list[RSSArticle] = []
                    if articles:
                        for article in articles:
                            full_link = page_def.prefix + article
                            scraped.append(self.article_scrape(ref=full_link))
                        page.articles = scraped
                        xml_page_save(page)
                    else:
                        logger.warning("no articles found")

            time.sleep(self.scrape_period * 60)

    def _get_resource(self, ref: str, local_file: bool = False) -> Article:
        article = Article(ref if not local_file else "")
        if local_file:
            with open(ref, "r", encoding="utf-8") as file:
                html = file.read()
                article.download(input_html=html)
        else:
            article.download(input_html=requests.get(ref, verify=False).text)
        return article

    def load_page_list(self) -> list[Path]:
        logger.debug(self.input_dir)
        return list(self.input_dir.rglob("*.html"))

    def index_load(self, ref: str, local_file: bool = False) -> BeautifulSoup:
        if local_file:
            logger.info(f"loading local {ref}")
            with open(ref, 'r') as index:
                return BeautifulSoup(index.read(), "html.parser")
        else:
            index = self._get_resource(ref=ref)
            return BeautifulSoup(index.html, "html.parser")

    def article_get(self, bs: BeautifulSoup, tag: str, designator: str) -> list[str]:
        """
        tag: str            html element (div/article/a)
        designator: str     css identificator of said element
        """
        hits = bs.find_all(tag, designator)
        logger.info(f"find all <{tag}> with '{designator}' designator: {hits}")

        hrefs = []
        for hit in hits:
            hrefs.extend([link['href'] for link in hit.find_all('a', href=True)])

        if not hrefs:
            logger.warning(bs)

        return hrefs[:self.article_limit]

    def page_scrape(self, ref: str, local_file: bool = False) -> RSSPage:
        logger.info(f"scrape page: {ref}")
        article = self._get_resource(ref=ref, local_file=local_file)
        article.parse()
        if self.use_nlp:
            logger.debug("using nlp")
            article.nlp()

        return RSSPage(
            title=article.title or "",
            link=ref,
            description=article.meta_description or "",
            language=article.meta_lang or "",
            pubDate=format_datetime(article.publish_date) if article.publish_date else "",
            category=", ".join(article.meta_keywords) if article.meta_keywords else "",
            image=article.top_image or "",
            managingEditor=article.authors[0] if article.authors else "",
            articles=[]
        )

    def article_scrape(self, ref: str, local_file: bool = False) -> RSSArticle:
        logger.info(f"scrape article: {ref}")
        article = self._get_resource(ref=ref, local_file=local_file)
        article.parse()
        if self.use_nlp:
            logger.debug("using nlp")
            article.nlp()

        doc = Document(article.html)
        clean_html = doc.summary()

        rss_article = RSSArticle(
            title=article.title,
            description=article.summary,
            content=clean_html,
            top_image=article.top_image,
            link=ref,
            author=article.authors,
            pubDate=format_datetime(article.publish_date) if article.publish_date else ""
        )
        return rss_article 


if __name__ == "__main__":
    pass
