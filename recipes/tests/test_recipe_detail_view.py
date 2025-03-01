from django.urls import reverse, resolve
from .test_recipe_base import RecipeTesteBase

from recipes import views


#testar as views da aplicaçao
#caso precisar de fazer um valor e so chamar o parametro correspondente
#exemplo assim: self.make_recipe(preparation_time=5)
class RecipeDetailViewTest(RecipeTesteBase):
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
    
    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """ test recipe is_published false not show the recipe """

        self.make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        
        self.assertEqual(response.status_code, 404)