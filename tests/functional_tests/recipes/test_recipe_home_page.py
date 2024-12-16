import pytest

from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest
from unittest.mock import patch




#isso e um marker que esta marcando como functional_test
#para por exemplo so rodas os testes que tem esse nome
@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.make_recipe_in_batch(qtd=20)
        self.browser.get(self.live_server_url)
        #seleciona o elemento no html
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.sleep()
        self.assertIn('No recipes found Here', body.text)




