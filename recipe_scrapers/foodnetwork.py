from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string


class FoodNetwork(AbstractScraper):

    @classmethod
    def host(self):
        return ['foodnetwork.com']

    def title(self):
        return self.soup.findAll('span', {'class': 'o-AssetTitle__a-HeadlineText'})[0].get_text()

    def total_time(self):
        return get_minutes(self.soup.find('dd', {'class': 'o-RecipeInfo__a-Description--Total'}))

    def ingredients(self):
        ingredients_html = self.soup.findAll('label', {'class': 'o-Ingredients__a-ListItemText'})

        return [
            normalize_string(ingredient.get_text())
            for ingredient in ingredients_html
            if ingredient.get_text(strip=True) not in ('Add all ingredients to list', '')
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('div', {'class': 'o-Method__m-Body'})

        return '\n'.join([
            normalize_string(instruction.get_text())
            for instruction in instructions_html
            if instruction.get_text(strip=True) not in ('Watch how to make this recipe.', '')
        ])

    def categories(self):
        categories_html = self.soup.findAll('a', {'class': 'o-Capsule__a-Tag a-Tag'})

        return [
            normalize_string(category.get_text())
            for category in categories_html
        ]
    
    def image_url(self):
        image_html = self.soup.find('meta', {'property': 'og:image'})
        return image_html['content']
