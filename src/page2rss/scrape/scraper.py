import time
import json
import requests
import urllib3
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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
                    page.title = nick
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

    def article_get_from_json_ld(self, bs: BeautifulSoup) -> list[str]:
        json_ld_scripts = bs.find_all('script', type='application/ld+json')

        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get('@type') == 'ItemList':
                    items = data.get('itemListElement', [])
                    urls = [item.get('url') for item in items if item.get('url')]
                    if urls:
                        logger.info(f"json-ld ItemList: {len(urls)}")
                        return urls
            except (json.JSONDecodeError, AttributeError, KeyError) as e:
                logger.debug(f"error parsing json-ld: {e}")
                continue

        return []

    def article_get_from_nextjs_data(self, bs: BeautifulSoup) -> list[str]:
        next_data = bs.find('script', id='__NEXT_DATA__')
        if not next_data:
            return []
        try:
            data = json.loads(next_data.string)
            urls = []
            def find_urls(obj, depth=0):
                if depth > 10: 
                    return
                if isinstance(obj, dict):
                    for key in ['url', 'link', 'href', 'permalink']:
                        if key in obj and isinstance(obj[key], str) and obj[key].startswith('http'):
                            urls.append(obj[key])
                    for value in obj.values():
                        find_urls(value, depth + 1)
                elif isinstance(obj, list):
                    for item in obj:
                        find_urls(item, depth + 1)

            find_urls(data)

            if urls:
                logger.info(f"next.js __next_data__: {urls}")
                return urls

        except (json.JSONDecodeError, AttributeError) as e:
            logger.debug(f"Error parsing Next.js data: {e}")

        return []

    def article_get_fallback(self, bs: BeautifulSoup) -> list[str]:
        all_links = bs.find_all('a', href=True)

        article_patterns = [
            '/article/', '/post/', '/news/', '/story/',
            '/blog/', '/-', '/20', '/201', '/202'  
        ]

        urls = []
        for link in all_links:
            href = link['href']
            if any(pattern in href for pattern in article_patterns):
                if href.startswith('http'):
                    urls.append(href)

        if urls:
            logger.info(f"fallback urls: {len(urls)}")
            return urls

        return []

    def article_get(self, bs: BeautifulSoup, tag: str = "", designator: str = "") -> list[str]:
        """
        tag: HTML element type (div/article/a) - optional
        designator: CSS selector/class name - optional

        strategy: 
        - both provided: find elements with specific tag AND class, extract hrefs strictly from them
        - only designator: find any elements with that class, get first href from child elements
        - neither: skip to auto-detection
        """
        hrefs = []

        if tag and designator:
            logger.info(f"searching with tag='{tag}' and class='{designator}'")
            hits = bs.find_all(tag, designator)
            logger.info(hits)

            if hits:
                for hit in hits:
                    if hit.name == 'a' and hit.get('href'):
                        hrefs.append(hit['href'])
                    else:
                        hrefs.extend([link['href'] for link in hit.find_all('a', href=True)])

                if hrefs:
                    logger.info(f"basic html (tag+class): {len(hrefs)}")
                    return hrefs[:self.article_limit]

        elif designator:
            logger.info(f"searching with class='{designator}' only (any tag)")
            hits = bs.find_all(class_=designator)
            logger.info(hits)

            if hits:
                for hit in hits:
                    if hit.name == 'a' and hit.get('href'):
                        hrefs.append(hit['href'])
                    else:
                        first_link = hit.find('a', href=True)
                        if first_link:
                            hrefs.append(first_link['href'])

                if hrefs:
                    logger.info(f"basic html (class only): {len(hrefs)}")
                    return hrefs[:self.article_limit]

        logger.info("try json-ld")
        hrefs = self.article_get_from_json_ld(bs)
        if hrefs:
            return hrefs[:self.article_limit]

        logger.info("try next.js __next_data__")
        hrefs = self.article_get_from_nextjs_data(bs)
        if hrefs:
            return hrefs[:self.article_limit]

        logger.info("try fallback pattern match")
        hrefs = self.article_get_fallback(bs)
        if hrefs:
            return hrefs[:self.article_limit]

        return []

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
