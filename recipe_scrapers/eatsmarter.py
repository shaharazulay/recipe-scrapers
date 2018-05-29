from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class EatSmarter(AbstractScraper):

    @classmethod
    def host(self):
        return ['eatsmarter.com']

    def title(self):
        return self.soup.find('meta', {'property': 'og:title'})['content']

    def categories(self):
        categories_html = self.soup.findAll('u1', {'class': 'tag-cloud-list'})

        return [
            normalize_string(category.get_text())
            for category in categories_html
        ]
    
