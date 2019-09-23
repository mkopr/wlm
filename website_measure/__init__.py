import logging
import os
import time

from website_measure.constants import LOG_FORMAT

# Set and create directions for non-relative files
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.normpath(os.path.join(SRC_DIR, ".."))
LOG_DIR_PATH = os.path.join(ROOT_DIR, 'logs')
LOG_FILE_PATH = os.path.join(
    LOG_DIR_PATH, 'wlm_{}.log'.format(time.strftime("%Y_%m_%d")),
)
try:
    os.mkdir(LOG_DIR_PATH)
except FileExistsError:
    pass

# Configure logger for app
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)


def run():
    from website_measure.main import WebsiteMeasure
    WebsiteMeasure().run()
