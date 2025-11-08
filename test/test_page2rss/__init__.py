import logging 

log_format = logging.Formatter(
    "%(asctime)s -> %(levelname)s"
    " \t[%(name)s][%(filename)s][L%(lineno)d]: %(message)s"
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)
