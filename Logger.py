"""
File: Logger.py
Version: 1.0
Author: Surender Kumar
Copyright @ *****
Contact: emailsurenderkumar@gmail.com

A custom logger to log the information. Ideally this should be a singleton
class, as one handler is sufficient to log the information.
"""

import logging

LOG_PATH = "."
LOG_FILE = "log.txt"
LOG_APP_NAME = "FlickrCrawler"

logger = logging.getLogger(LOG_APP_NAME)
logger.setLevel(logging.DEBUG)
# Handler to log debug messages
dbgH = logging.FileHandler(LOG_FILE)
dbgH.setLevel(logging.DEBUG)
# Handler for console
stdH = logging.StreamHandler()
stdH.setLevel(logging.ERROR)
# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
dbgH.setFormatter(formatter)
stdH.setFormatter(formatter)
# Adding handlers to the logger
logger.addHandler(dbgH)
logger.addHandler(stdH)

def getLogger():
    return logger
