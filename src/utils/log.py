import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)

log = logging.getLogger("megaton")
