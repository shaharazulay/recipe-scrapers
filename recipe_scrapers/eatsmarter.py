from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class EatSmarter(AbstractScraper):

    @classmethod
    def host(self):
        return ['eatsmarter.com']

    def title(self):
        return self.soup.find('meta', {'property': 'og:title'})['content']

    def categories(self):
        categories_html = self.soup.find('ul', {'class': 'tag-cloud-list'}).findAll('a')
        return [
            normalize_string(category.get_text())
            for category in categories_html
        ]

    def rating(self):
        return self.soup.find('span', {'class': 'average-rating'}).find('span').get_text()    

    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']
