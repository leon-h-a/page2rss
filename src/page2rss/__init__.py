import os
import logging 
from pathlib import Path

log_format = logging.Formatter(
    "%(asctime)s -> %(levelname)s"
    " \t[%(name)s][%(filename)s][L%(lineno)d]: %(message)s"
)

PROJECT_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__)))
PAGE_LIST: Path = PROJECT_ROOT / "data/page_list.json"
INPUT_DIR: Path = PROJECT_ROOT / "data/pages"
OUTPUT_DIR: Path = PROJECT_ROOT / "data/xml_output"

TEST_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "test/test_page2rss"
TEST_PAGE_LIST: Path = TEST_ROOT / "data/page_list.json"
TEST_INPUT_DIR: Path = TEST_ROOT / "data/pages"
TEST_OUTPUT_DIR: Path = TEST_ROOT / "data/xml_output"
