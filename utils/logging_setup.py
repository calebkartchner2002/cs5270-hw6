import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file: str = "consumer.log", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger("hw6-consumer")
    logger.setLevel(level)
    if not logger.handlers:
        fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s - %(message)s")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger
