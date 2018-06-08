import re

from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return ['allrecipes.com']

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return get_minutes(self.soup.find('span', {'class': 'ready-in-time'}))

    def ingredients(self):
        ingredients_html = self.soup.findAll('span', {'class': "recipe-ingred_txt added"})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
            if ingredient.get_text(strip=True) not in ('Add all ingredients to list', '')
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('span', {'class': 'recipe-directions__list--item'})

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])

    def categories(self):
        categories_html = self.soup.findAll('meta', {'itemprop': 'recipeCategory'})

        return [
            normalize_string(category['content'])
            for category in categories_html
        ]

    def rating(self):
        rating_html = self.soup.find('meta', {'property': 'og:rating'})
        return rating_html['content']
    
    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']

    
class AllRecipesUKAsia(AbstractScraper):

    @classmethod
    def host(self):
        return ['allrecipes.co.uk', 'allrecipes.asia']

    def title(self):
        return self.soup.find('h1').get_text()

    def total_time(self):
        return get_minutes(self.soup.find('span', {'class': 'ready-in-time'}))

    def ingredients(self):
        ingredients_html = self.soup.findAll('span', {'class': "recipe-ingred_txt added"})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
            if ingredient.get_text(strip=True) not in ('Add all ingredients to list', '')
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('span', {'class': 'recipe-directions__list--item'})

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
        ])

    def categories(self):
        script = self.soup.find('script', text=lambda x: 'pageTargetingValues' in str(x))
        match = re.findall('h: \\[.*\\]', script.text)[-1]
        categories = eval(re.findall('\\[.*\\]', match)[-1])

        return categories

    def rating(self):
        rating_html = self.soup.find('meta', {'itemprop': 'ratingValue'})
        return rating_html['content']

