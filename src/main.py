from sreality_crawler import Crawler
from sreality_dao import SRealityDao
from sreality_parser import Parser

def main():
    dao = SRealityDao("", "", "", "")
    parser = Parser()
    crawler = Crawler(dao, parser)

main()