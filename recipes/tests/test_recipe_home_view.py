from django.urls import reverse, resolve
from .test_recipe_base import RecipeTesteBase
from unittest.mock import patch

from recipes import views


#testar as views da aplicaçao
#caso precisar de fazer um valor e so chamar o parametro correspondente
#exemplo assim: self.make_recipe(preparation_time=5)
class RecipeHomeViewTest(RecipeTesteBase):
    def test_recipe_home_view_function_is_correct(self):
        #detecta qual view esta, e o reverse pega a url para deixa-la aqui dinamica
        view = resolve(reverse('recipes:recipes-home'))
        #compara as duas views se sao iguais usando o is, ou seja se esta apontando para a
        #mesma locaçao de memoria
        self.assertIs(view.func, views.home)
    
    def test_recipe_home_view_returns_status_200_OK(self):
        #ele vai pegar o get, da url e retornar o status
        response = self.client.get(reverse('recipes:recipes-home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:recipes-home'))
        #passar esse asserttemplateused para fazer a compararaçao 
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipes-home'))
        self.assertIn(
            '<h1>No recipes found Here<h1>',
            response.content.decode('utf-8')
        )
    
    #teste com conteudo na home
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:recipes-home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('10 minutos', content)
        self.assertIn('5 porçoes', content)
        self.assertEqual(len(response_context_recipes), 1)
    
    def teste_recipe_home_template_dont_load_recipes_not_published(self):
        """ test recipe is_published false not show the recipe """

        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipes-home'))
        self.assertIn(
            '<h1>No recipes found Here<h1>',
            response.content.decode('utf-8')
        )
    
    #test mockado
    # test mockado seria uma simulaçao ne uma variavel que n pode ser mudada por algum
    #motivo no caso aki seria PER_PAGE
    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new = 3):
            response = self.client.get(reverse('recipes:recipes-home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            #nessa pagina 1 deve ter 3 receita na 2 e na 3 tbm respectivamente
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
