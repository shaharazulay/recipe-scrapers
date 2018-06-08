from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class SeriousEats(AbstractScraper):

    @classmethod
    def host(self):
        return ['seriouseats.com']

    def title(self):
        return self.soup.find('meta', {'property': 'og:title'})['content']

    def categories(self):
        categories_html = self.soup.find('ul', {'class': 'tags'}).findAll('a')
        return [
            normalize_string(category.get_text())
            for category in categories_html
        ]

    def rating(self):
        return self.soup.find('meta', {'itemprop': 'ratingValue'})['content']

    def review_count(self):
        return self.soup.find('meta', {'itemprop': 'reviewCount'})['content']

    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']
