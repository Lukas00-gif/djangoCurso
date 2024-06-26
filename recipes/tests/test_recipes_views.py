from django.urls import reverse, resolve
from .test_recipe_base import RecipeTesteBase

from recipes import views


#testar as views da aplicaçao
#caso precisar de fazer um valor e so chamar o parametro correspondente
#exemplo assim: self.make_recipe(preparation_time=5)
class RecipeViewsTest(RecipeTesteBase):
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


    #category
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        #ele vai pegar o get, da url e retornar o status
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)
    
    def teste_recipe_category_template_dont_load_recipes_not_published(self):
        """ test recipe is_published false not show the recipe """

        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        
        self.assertEqual(response.status_code, 404)
    

    #detail
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
            )
        self.assertIs(view.func, views.repice)
    
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        #ele vai pegar o get, da url e retornar o status
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_recipe_detail_template_loads_the_correct_recipes(self):
        needed_title = 'This is a detail page - It load one recipe'
        self.make_recipe(title=needed_title)
        
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)
    
    def teste_recipe_detail_template_dont_load_recipe_not_published(self):
        """ test recipe is_published false not show the recipe """

        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        
        self.assertEqual(response.status_code, 404)
