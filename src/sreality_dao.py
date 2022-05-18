from mysql.connector import (connection)

class SRealityDao:

    INSERT_OFFER_QUERY = "insert into offer_orig(url, sreality_id, disposition, price, area) values (%(url)s, %(sreality_id)s, %(disposition)s, %(price)s, %(area)s);"
    INSERT_LINK_TO_DOWNLOAD_QUERY = "insert into to_download(url) values(%(url)s);"
    URL_TO_DOWNLOAD_QUERY = "select id, url from to_download limit 1"
    ALL_URLS_TO_DOWNLOAD_QUERY = "select url from to_download"
    REMOVE_DOWNLOADED_QUERY = "delete from to_download where id=%s"
    

    def __init__(self, dbConfig):
        self.config = dbConfig
        self.cnx = None
        self.cursor = None
    
    def getAllLinksToDownload(self):
        existingLinks = []
        self._createDbContext()
        self.cursor.execute(self.ALL_URLS_TO_DOWNLOAD_QUERY)

        for (url,) in self.cursor:
            existingLinks.append(url)

        self._commitAndClose

        return existingLinks
    
    def saveDownloadedOffer(self, offer):
        """
        Save parsed data to DB.
        """
        self._createDbContext()
        print(offer)
        self.cursor.execute(self.INSERT_OFFER_QUERY, offer)
        self._commitAndClose()

    def saveNewLinks(self, newOfferLinks):
        self._createDbContext()
        for link in newOfferLinks:
            self.cursor.execute(self.INSERT_LINK_TO_DOWNLOAD_QUERY, link)
        self._commitAndClose()
        return newOfferLinks
    
    def removeDownloaded(self, id):
        """
        Remove url from to_download that has been downloaded. 
        """
        self._createDbContext()
        self.cursor.execute(self.REMOVE_DOWNLOADED_QUERY, (int(id),))
        self._commitAndClose()

    def selectUrlToDownload(self):
        """
        Select first available item to download from DB.
        """
        toDownload = []
        self._createDbContext()

        self.cursor.execute(self.URL_TO_DOWNLOAD_QUERY)

        for (id,url) in self.cursor:
            toDownload.append({'id': id, 'url': url})

        self._commitAndClose()

        return toDownload[0] if len(toDownload) > 0 else None

    def _createDbContext(self):
        self.cnx = connection.MySQLConnection(**self.config)
        self.cursor = self.cnx.cursor()
    
    def _commitAndClose(self):
        self.cnx.commit()
        self.cursor.close()
        self.cnx.close()
