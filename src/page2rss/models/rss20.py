from dataclasses import dataclass, field
from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from page2rss.models import logger


@dataclass
class RSSArticle:
    """
    RSS 2.0 spec
    """
    title: str
    description: str = ""

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

        rss_item = ET.Element("item")

        title = ET.SubElement(rss_item, "title")
        title.text = escape(self.title)

        link = ET.SubElement(rss_item, "link")
        link.text = escape(self.link)

        desc = ET.SubElement(rss_item, "description")
        desc.text = escape(self.description)

        content_html = self.content
        if self.top_image:
            top_img = f"<p><img src='{self.top_image}' alt='top image'></p>"
            content_html = top_img + content_html

        content = ET.SubElement(rss_item, "content:encoded")
        content.text = f"<![CDATA[{content_html}]]>"

        if self.author:
            author = ET.SubElement(rss_item, "author")
            author.text = escape(", ".join(self.author))

        if self.category:
            category = ET.SubElement(rss_item, "category")
            category.text = escape(self.category)

        if self.pubDate:
            pub_date = ET.SubElement(rss_item, "pubDate")
            pub_date.text = escape(self.pubDate)

        parsed = ET.tostring(rss_item, encoding="utf-8").decode("utf-8")
        logger.debug(f"xml <item> {parsed}")

        return parsed


@dataclass
class RSSPage:
    """
    RSS 2.0 spec
    """
    title: str
    link: str
    description: str

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
        content = "<channel>" + "".join(a.xml() for a in self.articles) + "</channel>"

        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0"
                 xmlns:content="http://purl.org/rss/1.0/modules/content/">
              <channel>
                {content}
              </channel>
        </rss>
        """
