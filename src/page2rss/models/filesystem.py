from dataclasses import dataclass


@dataclass
class PageEntry:
    nick: str = ""
    url: str = ""
    tag: str = ""
    css: str = ""
    prefix: str = ""
