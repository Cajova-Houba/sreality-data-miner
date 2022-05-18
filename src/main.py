from sreality_crawler import Crawler
from sreality_dao import SRealityDao
from sreality_parser import Parser
import configparser

def loadDbConfig(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)
    return config['Database']

def main():
    dbConfig = loadDbConfig("config.ini")
    dao = SRealityDao(dbConfig)
    parser = Parser()
    crawler = Crawler(dao, parser)

    crawler.searchNewOffers()
    crawler.processNewOffers()

main()
