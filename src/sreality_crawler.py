from selenium import webdriver 
import time

class Crawler:

    searchUrl = "https://www.sreality.cz/hledani/prodej/byty?strana=%d"
    politenessTime = 0.5
    maxSearchPage = 10000
    pageNotFoundMessage = "Je mi líto, stránka neexistuje."

    def __init__(self, dao, parser):
        self.dao = dao
        self.parser = parser
        self.browser = self._createHeadlessBrowser()
    
    def searchNewOffers(self):
        """
        Search new offers at sreality.cz and save their urls.
        """
        finalPage = False
        currentPage = 1

        while(currentPage <= self.maxSearchPage and not(finalPage)):
            print("Downloading search results, page=%d" % currentPage)
            content = self._downloadPage(self.searchUrl % currentPage)
            finalPage = self._isFinalSearchPage(content)
            self._saveNewLinks(content)
            currentPage = currentPage+1
            self._politeWait()

    def _downloadPage(self, url):
        """
        Download the page given by url and return its content.
        """

        self.browser.get(url)
        return self.browser.page_source
    
    def _saveNewLinks(self, content): 
        newOfferLinks = self.parser.parseSearchPage(content)
        existingLinks = self.dao.getAllLinksToDownload()
        linksToSave = self.dao.filterExistingLinks(newOfferLinks, existingLinks)
        self.dao.saveNewLinks(linksToSave)

    def _filterExistingLinks(self, newOfferLinks, existingLinks):
        return list(
            filter(
                lambda new: not(new in existingLinks), 
                newOfferLinks
            )
        )

    def _isFinalSearchPage(self, content):
        """
        Determine whether the search page is the last one by its content.
        """
        return self.pageNotFoundMessage in content

    def _politeWait(self):
        time.sleep(self.politenessTime)  

    def _createHeadlessBrowser(self):
        """
        Create and return instance of a Selenium headless browser.
        """
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True
        return webdriver.Firefox(options=fireFoxOptions)

