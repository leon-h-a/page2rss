import os
from pathlib import Path
from xml.dom import minidom
from page2rss import OUTPUT_DIR
from page2rss.models.rss20 import RSSPage
from page2rss.filesystem import logger


def xml_page_save(page: RSSPage, output_dir: Path = OUTPUT_DIR) -> None:
    pprint = minidom.parseString(page.xml()).toprettyxml(indent="  ")

    filename = page.title.replace(" " ,"_") + ".xml"
    logger.info(f"sanitize '{page.title}' to '{filename}'")

    with open(output_dir / filename, "w", encoding="utf-8") as f:
        f.write(pprint)
    logger.info(f"successful save {str(output_dir / filename)}")


def xml_page_remove(filename: str, output_dir: Path = OUTPUT_DIR)  -> None:
    try:
        os.remove(output_dir / filename)
        logger.info(f"file removed {str(output_dir / filename)}")
    except FileNotFoundError:
        logger.warning(f"file not found {str(output_dir / filename)}")


if __name__ == "__main__":
    pass
