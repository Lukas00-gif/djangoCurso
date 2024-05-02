from django.test import TestCase
from django.urls import reverse, resolve


from recipes import views



#testar as views da aplicaçao
class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        #detecta qual view esta, e o reverse pega a url para deixa-la aqui dinamica
        view = resolve(reverse('recipes:recipes-home'))
        #compara as duas views se sao iguais usando o is, ou seja se esta apontando para a
        #mesma locaçao de memoria
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
            )
        self.assertIs(view.func, views.repice)
        
