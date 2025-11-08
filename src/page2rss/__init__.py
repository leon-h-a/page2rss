import os
import logging 
from pathlib import Path

log_format = logging.Formatter(
    "%(asctime)s -> %(levelname)s"
    " \t[%(name)s][%(filename)s][L%(lineno)d]: %(message)s"
)

PROJECT_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR: Path = PROJECT_ROOT / "pages"
OUTPUT_DIR: Path = PROJECT_ROOT / "xml_output"

TEST_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "test/test_page2rss"
TEST_INPUT_DIR: Path = TEST_ROOT / "pages"
TEST_OUTPUT_DIR: Path = TEST_ROOT / "xml_output"
