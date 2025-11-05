from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from page2rss.models.models import RSSArticle
from page2rss.xml import logger


class XML:
    def __init__(self):
        pass

    def xml_generate_item(self, article: RSSArticle) -> str:
        logger.debug(f"xml generate <item> from {article}")

        rss_item = ET.Element("item")

        title = ET.SubElement(rss_item, "title")
        title.text = escape(article.title)

        link = ET.SubElement(rss_item, "link")
        link.text = escape(article.link)

        desc = ET.SubElement(rss_item, "description")
        desc.text = escape(article.description)

        content_html = article.content
        if article.top_image:
            top_img = f"<p><img src='{article.top_image}' alt='top image'></p>"
            content_html = top_img + content_html

        content = ET.SubElement(rss_item, "content:encoded")
        content.text = f"<![CDATA[{content_html}]]>"

        if article.author:
            author = ET.SubElement(rss_item, "author")
            author.text = escape(", ".join(article.author))

        if article.category:
            category = ET.SubElement(rss_item, "category")
            category.text = escape(article.category)

        if article.pubDate:
            pub_date = ET.SubElement(rss_item, "pubDate")
            pub_date.text = escape(article.pubDate)

        parsed = ET.tostring(rss_item, encoding="utf-8").decode("utf-8")
        logger.debug(f"xml <item> {parsed}")

        self._file_save(parsed)

        return parsed

    def _file_save(self, content: str) -> None:
        logger.debug(f"xml <item> save")

        wrapped = f"""<?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0"
                 xmlns:content="http://purl.org/rss/1.0/modules/content/">
              <channel>
                {content}
              </channel>
        </rss>
        """

        logger.info(wrapped)

        pprint = minidom.parseString(wrapped).toprettyxml(indent="  ")
        with open("/some/path/a.xml", "w", encoding="utf-8") as f:
            f.write(pprint)


    def xml_generate_page(self, xml_items: list[str]) -> str:
        pass

    def teardown(self):
        pass


if __name__ == "__main__":
    pass
