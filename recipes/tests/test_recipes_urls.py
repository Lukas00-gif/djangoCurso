from django.test import TestCase
from django.urls import reverse



# testar as url da aplicaçao
class RecipeURLsTest(TestCase):
    def test_recipe_home_is_correct(self):
        #pega a url da home usando o reverse(de dentro para fora da aplicaçao)
        url = reverse('recipes:recipes-home')
        #e compara com a barra, se for a mesma ele vai passar
        self.assertEqual(url, '/')
        
    def test_recipe_category_is_correct(self):
        #neste caso e a mesma coisa so que tem q passar por kwargs a category:id
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_is_correct(self):
        url = reverse('recipes:recipe', kwargs={'pk': 1})
        self.assertEqual(url, '/recipes/1/')
    
    # TDD onde voce faz os testes primeiro e depois desenvolve
    #RED - GREEN - REFACTOR
    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')