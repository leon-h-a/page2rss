import os
import logging 
from pathlib import Path

log_format = logging.Formatter(
    "%(asctime)s -> %(levelname)s"
    " \t[%(name)s][%(filename)s][L%(lineno)d]: %(message)s"
)

PROJECT_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR: Path = PROJECT_ROOT / "data"

TEST_ROOT: Path = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent / "test"
TEST_DATA_DIR: Path = TEST_ROOT / "data"
