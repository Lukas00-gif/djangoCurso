from django.urls import reverse, resolve
from .test_recipe_base import RecipeTesteBase

from recipes import views


#testar as views da aplicaçao
#caso precisar de fazer um valor e so chamar o parametro correspondente
#exemplo assim: self.make_recipe(preparation_time=5)
class RecipeDetailViewTest(RecipeTesteBase):
    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, views.RecipeListViewSearch)
    
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search')+ '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
    
    def test_recipe_search_raises_404_if_no_seach_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
    
    #tem que ser exatamente igual
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &lt;Teste&gt;',
            response.content.decode('utf-8')
        )
    
    # def test_recipe_search_can_find_recipe_by_title(self):
    #     title1 = 'This is recipe one'
    #     title2 = 'This is recipe two'
        
    #     recipe1 = self.make_recipe(
    #         slug='one', title='title1', author_data={ 'username': 'one' }
    #     )       

    #     recipe2 = self.make_recipe(
    #         slug='two', title='title2', author_data={ 'username': 'two' }
    #     )

    #     search_url = reverse('recipes:search')
    #     response1 = self.client.get(f'{ search_url }?q={title1}')

    #     self.assertIn(recipe1, response1.context['recipes'])



