import sys
from loguru import logger

# Time stamps not required.
logger.remove()
logger.add(sys.stderr, format="<level>{level}: {message}</level>\n")
