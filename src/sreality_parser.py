from bs4 import BeautifulSoup
import re

class Parser:

    offerLinkRegex = "/detail/prodej/byt/[a-zA-Z+0-9]+/[a-zA-Z+0-9-_]+/\d+"
    idFromUrlRegex = r".*/(\d+)"
    dispositionFromUrlRegex = r".*\/([\d+k]+|atypicky)\/"

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

    def parseAdPage(self, pageContent, url):
        """
        Parse raw data from advertisement page content and its url.
        """

        soup = BeautifulSoup(pageContent, 'html.parser')
        parsed = {
            'url': url,
            'sreality_id': self.parseFromUrl(url, self.idFromUrlRegex),
            'disposition': self.parseFromUrl(url, self.dispositionFromUrlRegex)
        }

        items = soup.find_all("li", {"class": "param ng-scope"})
        for item in items:
            name = ""
            value = ""
            for child in item.findChildren("label"):
                name = child.getText()
            
            for child in item.findChildren("span"):
                value = value + child.getText()
            
            parsed[self.nameToProperty(name)] = value


        return parsed
    
    def parseFromUrl(url, regex):
        m = re.match(regex, url)
        if m:
            return m.group(1)
        else:
            return 'could not parse'

    def nameToProperty(name):
        """
        Sreality ad property name -> enum like value
        """
        if (name == "Celková cena:") or (name == "Zlevněno:") or (name == "Původní cena:"):
            return "price"
        elif (name == "Užitná plocha:"):
            return "area"
        else:
            return name