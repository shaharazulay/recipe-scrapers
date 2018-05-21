try:
    from urllib import request
except:
    from urllib2 import urlopen as request
    from urllib2 import Request

from bs4 import BeautifulSoup
from requests.models import Response


class AbstractScraper(object):

    def __init__(self, resp, test=False):

        self._valid = True
        if (resp is None) or (resp.status_code != 200):
            self.soup = None
            self._valid = False
            self.doc = None
        else:
            self.doc = resp.text
            self.soup = BeautifulSoup(resp.text, "html.parser")

    @classmethod
    def from_dump(cls, doc):
        resp = Response()
        resp.status_code = 200
        resp._content = doc.encode('utf-8')
        return cls(resp)

    def content(self):
        return self.doc
    
    def is_valid(self):
        return self._valid
    
    def host(self):
        """ get the host of the url, so we can use the correct scraper (check __init__.py) """
        raise NotImplementedError("This should be implemented.")

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def servings(self):
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """ total time it takes to preparate the recipe in minutes """
        raise NotImplementedError("This should be implemented.")

    def ingredients(self):
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
        raise NotImplementedError("This should be implemented.")
