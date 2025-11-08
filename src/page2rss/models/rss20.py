from dataclasses import dataclass, field
from lxml import etree
from page2rss.models import logger

CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"


@dataclass
class RSSArticle:
    """
    RSS 2.0 spec
    """
    # mandatory
    title: str
    description: str = ""

    # non-mandatory
    link: str = ""
    author: str = ""
    category: str = ""
    comments: str = ""
    enclosure: str = ""
    guid: str = ""
    pubDate: str = ""
    source: str = ""

    # non-spec 
    top_image: str = ""
    content: str = "" # used for <content:encoded> in xml output

    def xml(self) -> str:
        logger.info(f"xml generate <item> from {self.title}")

        nsmap = {'content': CONTENT_NS}
        rss_item = etree.Element("item", nsmap=nsmap)

        title = etree.SubElement(rss_item, "title")
        title.text = self.title

        link = etree.SubElement(rss_item, "link")
        link.text = self.link

        desc = etree.SubElement(rss_item, "description")
        desc.text = self.description

        content_html = self.content
        if self.top_image:
            top_img = f"<p><img src='{self.top_image}' alt='top image'></p>"
            content_html = top_img + content_html

        content = etree.SubElement(rss_item, f"{{{CONTENT_NS}}}encoded")
        content.text = etree.CDATA(content_html)

        if self.author:
            author = etree.SubElement(rss_item, "author")
            author.text = ", ".join(self.author)

        if self.category:
            category = etree.SubElement(rss_item, "category")
            category.text = self.category

        if self.pubDate:
            pub_date = etree.SubElement(rss_item, "pubDate")
            pub_date.text = self.pubDate

        parsed = etree.tostring(rss_item, encoding="utf-8").decode("utf-8")
        logger.debug(f"xml <item> {parsed}")

        return parsed


@dataclass
class RSSPage:
    """
    RSS 2.0 spec
    """
    # mandatory
    title: str
    link: str
    description: str

    # non-mandatory
    language: str = ""
    copyright: str = ""
    managingEditor: str = ""
    webMaster: str = ""
    pubDate: str = ""
    lastBuildDate: str = ""
    category: str = ""
    generator: str = ""
    docs: str = ""
    cloud: str = ""
    ttl: str = ""
    image: str = ""
    rating: str = ""
    textInput: str = ""
    skipHours: str = ""
    skipDays: str = ""

    # non-spec
    articles: list[RSSArticle] = field(default_factory=list)

    def xml(self) -> str:
        logger.info(f"xml generate <page> from {self.title}")

        nsmap = {'content': CONTENT_NS}

        rss = etree.Element("rss", version="2.0", nsmap=nsmap)
        channel = etree.SubElement(rss, "channel")

        title = etree.SubElement(channel, "title")
        title.text = self.title

        link = etree.SubElement(channel, "link")
        link.text = self.link

        description = etree.SubElement(channel, "description")
        description.text = self.description

        if self.language:
            language = etree.SubElement(channel, "language")
            language.text = self.language

        if self.copyright:
            copyright_elem = etree.SubElement(channel, "copyright")
            copyright_elem.text = self.copyright

        if self.managingEditor:
            managing_editor = etree.SubElement(channel, "managingEditor")
            managing_editor.text = self.managingEditor

        if self.webMaster:
            web_master = etree.SubElement(channel, "webMaster")
            web_master.text = self.webMaster

        if self.pubDate:
            pub_date = etree.SubElement(channel, "pubDate")
            pub_date.text = self.pubDate

        if self.lastBuildDate:
            last_build_date = etree.SubElement(channel, "lastBuildDate")
            last_build_date.text = self.lastBuildDate

        if self.category:
            category = etree.SubElement(channel, "category")
            category.text = self.category

        if self.generator:
            generator = etree.SubElement(channel, "generator")
            generator.text = self.generator

        if self.ttl:
            ttl = etree.SubElement(channel, "ttl")
            ttl.text = self.ttl

        for article in self.articles:
            item_element = etree.fromstring(article.xml())
            channel.append(item_element)

        return etree.tostring(
            rss,
            encoding="utf-8",
            xml_declaration=True,
            pretty_print=True
        ).decode("utf-8")
