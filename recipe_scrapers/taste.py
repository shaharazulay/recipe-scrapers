from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class Taste(AbstractScraper):

    @classmethod
    def host(self):
        return ['taste.com.au']

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients_html = self.soup.findAll('div', {'class': 'ingredient-description'})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('div', {'class': 'recipe-method-step-content'})

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])

    def categories(self):
        categories_html = self.soup.findAll('meta', {'name': 'keywords'})

        return [
            normalize_string(c) for category in categories_html
            for c in category['content'].split(',')
        ]
    
    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']
