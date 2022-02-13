from bs4 import BeautifulSoup
import re

class Parser:

    offerLinkRegex = "/detail/prodej/byt/[a-zA-Z+0-9]+/[a-zA-Z+0-9-_]+/\d+"

    def parseSearchPage(self, pageContent):
        """
        Use BeautifulSoup library to parse the HTML
        content of one search list page and return 
        list of links to ads.
        """
        soup = BeautifulSoup(pageContent, 'html.parser')
        adLinks = []

        items = soup.find_all("a", href=re.compile(self.offerLinkRegex))
        for item in items:
            itemLink = item['href']
            adLinks.append(itemLink)

        return adLinks