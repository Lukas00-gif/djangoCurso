from .test_recipe_base import RecipeTesteBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTesteBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_defauls(self):
        recipe = Recipe(
            #os nomes devem ser diferentes
            category = self.make_category(name='Test Default Category'),
            author = self.make_author(username='newusername'),    
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'Recipe-slug',
            preparation_time = '10',
            preparation_time_unit = 'minutos',
            servings = '5',
            servings_unit = 'porçoes',
            preparation_step = 'Recipe preparation step',
            cover = 'teste'
        )
        recipe.full_clean()
        recipe.save()
        return recipe
    
    #faz com que gere o erro
    #tem que envolver pegar o erro para levantar o erro
    def test_recipe_title_raise_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    
    '''para nao ficar repetindo muito o codigo podemos fazer um for para nao ficar
    repetindo codigo novamente
    usando o parameterized da para fazer um grupo de teste usando ele
    assim criando testes separadados
    '''
    @parameterized.expand(
        [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 20),
            ('servings', 20),
            ('servings_unit', 20),
        ]
    )

    def test_recipe_fields_max_lenght(self, field, max_lenght):
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
    
    # testar isso e valido ja que o false no default ele muda a estrutura logica
    # do model
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defauls()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.preparation_step_is_html,
                        msg='preparations steps in model is not True is False for default')
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defauls()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(recipe.is_published,
                        msg='is published in model is not True is False for default')
    
    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Represetation'
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(str(self.recipe), 'Testing Represetation')




