import logging
import pathlib

formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s (%(funcName)s) | %(message)s'
)
filename = pathlib.Path(__file__).resolve().parent.parent / "log.log"
fh = logging.FileHandler(str(filename), encoding="utf-8")
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

logger = logging.getLogger("lotto")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
