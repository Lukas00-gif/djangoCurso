import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch



#isso e um marker que esta marcando como functional_test
#para por exemplo so rodas os testes que tem esse nome
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.make_recipe_in_batch(qtd=10)
        self.browser.get(self.live_server_url)
        #seleciona o elemento no html
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()    
        self.assertIn('No recipes found Here', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        #usuario abri a pagina
        self.browser.get(self.live_server_url)
        
        #ve o input com o campo de busca "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH, 
            '//input[@placeholder="Search for a recipe..."]'
        )

        #clicar nesse input e digita o termo de busca
        # para encontrar a receita com o titulo desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        #usuario ve o que esta o que esta procurando na pagina
        self.assertIn(
            title_needed,
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

        self.sleep(5)
    

    @patch('recipes.views.PER_PAGE', new=2)
    def test_home_page_pagination(self):
        recipes = self.make_recipe_in_batch()

        # usuario abri a pagina
        self.browser.get(self.live_server_url)

        # ve que tem paginaçao e clica na pagina 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go To page 2"]'
        )
        page2.click()

        # Ve que tem mais duas receitas na pagina 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )

        self.sleep(5)




