import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

# Change logging level here.
logger.setLevel(int(os.environ.get("LOG_LEVEL", logging.WARNING)))
