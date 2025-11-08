import os
import json
import tempfile
import traceback
from pathlib import Path
from xml.dom import minidom
from page2rss import PAGE_LIST, OUTPUT_DIR
from page2rss.models.rss20 import RSSPage
from page2rss.models.filesystem import PageEntry 
from page2rss.filesystem import logger


def xml_page_save(page: RSSPage, output_dir: Path = OUTPUT_DIR) -> None:
    pprint = minidom.parseString(page.xml()).toprettyxml(indent="  ")

    filename = page.title.replace(" " ,"_") + ".xml"
    logger.info(f"sanitize '{page.title}' to '{filename}'")

    fd, t_path = tempfile.mkstemp(
        dir=output_dir, prefix=".tmp."
    ) 
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(pprint)
        os.replace(t_path, output_dir / filename)
        logger.info(f"successful save {str(output_dir / filename)}")

    except Exception:
        logger.warning(traceback.format_exc())


def xml_page_remove(filename: str, output_dir: Path = OUTPUT_DIR)  -> None:
    try:
        os.remove(output_dir / filename)
        logger.info(f"file removed {str(output_dir / filename)}")
    except FileNotFoundError:
        logger.warning(f"file not found {str(output_dir / filename)}")

def page_def_list(page_list_dir: Path = PAGE_LIST) -> list[str]:
    with open(page_list_dir, "r") as pgl:
        return list(json.load(pgl))

def page_def_read(nick: str, page_list_dir: Path = PAGE_LIST) -> PageEntry | None:
    with open(page_list_dir, "r") as pgl:
        page_list = dict(json.load(pgl))

    try:
        page_def_raw = page_list[nick]
        page_def = PageEntry(
            url=page_def_raw["url"],
            tag=page_def_raw["tag"],
            css=page_def_raw["css"],
            prefix=page_def_raw["prefix"]
        )
        logger.info(page_def)
        return page_def

    except KeyError:
        logger.warning(f"page {nick} not found in page def list")
        return None


def page_def_update(page: PageEntry, page_list_dir: Path = PAGE_LIST) -> bool:
    with open(page_list_dir, "r") as pgl:
        page_list = dict(json.load(pgl))
        page_list[page.nick] = dict(
            url=page.url,
            tag=page.tag,
            css=page.css,
            prefix=page.prefix
        )

    fd, t_path = tempfile.mkstemp(dir=page_list_dir.parent, suffix=".tmp.") 
    try:
        with os.fdopen(fd, "a", encoding="utf-8") as pgl:
            pgl.write(json.dumps(page_list, indent=2))

        os.replace(t_path, page_list_dir) 
        logger.info(f"successful update page list with {page}")
        return True

    except Exception:
        logger.warning(traceback.format_exc())
        return False


def page_def_remove(page: PageEntry, page_list_dir: Path = PAGE_LIST) -> bool:
    with open(page_list_dir, "r") as pgl:
        page_list = dict(json.load(pgl))

    try:
        del page_list[page.nick]
    except KeyError:
        logger.warning(f"page {page} not found in page list")
        return False

    fd, t_path = tempfile.mkstemp(dir=page_list_dir.parent, suffix=".tmp.") 
    try:
        with os.fdopen(fd, "a", encoding="utf-8") as pgl:
            pgl.write(json.dumps(page_list))

        os.replace(t_path, page_list_dir) 
        logger.info(f"successful remove {page} from page list with")
        return True

    except Exception:
        logger.warning(traceback.format_exc())
        return False


if __name__ == "__main__":
    pass
