# -*- coding: utf-8
from sreality_crawler import Crawler
from sreality_dao import SRealityDao
from sreality_parser import Parser
import configparser
import logging

logging.basicConfig(filename='crawler.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("crawler_main")


def loadDbConfig(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)
    return config['Database']

def main():
    logger.info("Starting crawler")
    dbConfig = loadDbConfig("config.ini")
    logger.info("Config parsed")
    dao = SRealityDao(dbConfig)
    parser = Parser()
    crawler = Crawler(dao, parser)

    logger.info("Searching for new offers")
    try:
        crawler.searchNewOffers()
    except:
        logger.exception("Unexpected exception while searching for new offers:")
        return

    logger.info("Processing new offers")
    try:
        crawler.processNewOffers()
    except:
        logger.exception("Unexpected exception while processing new offers:")
        return

    logger.info("Done, exiting crawler")


main()
