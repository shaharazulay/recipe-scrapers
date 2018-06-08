from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class Epicurious(AbstractScraper):

    @classmethod
    def host(self):
        return ['epicurious.com']

    def title(self):
        return self.soup.find('h1', {'itemprop': 'name'}).get_text()

    def total_time(self):
        return get_minutes(self.soup.findAll('p', {'class': 'summary_data'})[-1])

    def ingredients(self):
        ingredients_html = self.soup.findAll('li', {'itemprop': "ingredients"})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
        ]

    def instructions(self):
        instructions_html = self.soup.find('div', {'id': 'preparation'}).find_all('p')

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])

    def categories(self):
        categories_html = self.soup.findAll('meta', {'itemprop': 'keywords'})
        
        return [
            normalize_string(c) for category in categories_html
            for c in category['content'].split(',')
        ]

    def rating(self):
        return self.soup.find('span', {'class': 'rating'}).get_text()
        
    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']
