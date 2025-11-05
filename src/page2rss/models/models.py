from dataclasses import dataclass


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
