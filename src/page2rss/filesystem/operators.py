import os
import tempfile
import traceback
from pathlib import Path
from xml.dom import minidom
from page2rss import OUTPUT_DIR
from page2rss.models.rss20 import RSSPage
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


if __name__ == "__main__":
    pass
