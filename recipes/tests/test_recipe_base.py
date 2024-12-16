from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)
    
    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@gmail.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
    
    def make_recipe(
            self,
            category_data = None,
            author_data = None,    
            title = 'Recipe Title',
            description = 'Recipe Description',
            slug = 'Recipe-slug',
            preparation_time = '10',
            preparation_time_unit = 'minutos',
            servings = '5',
            servings_unit = 'porçoes',
            preparation_step = 'Recipe preparation step',
            preparation_step_is_html = False,
            is_published = True,
            cover = 'teste'
    ):
        #vai verificar se o category data e None se for ele atribui um dicionario vazio
        if category_data is None :
            category_data = {}
        
        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            #como e um dic vazio e so fazer desacompamento de dados **category_data
            # que ele faz automatico
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),    
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_step = preparation_step,
            preparation_step_is_html = preparation_step_is_html,
            is_published = is_published,
            cover = cover
        )
    
    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {
                        'title': f'Recipe Title {i}',
                        'slug': f'r{i}', 
                        'author_data': {'username': f'u{i}'}
                    }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


#aqui e a base serve para serpar as classes e fazer reutilizar das mesmas
# ou seja separando as classes dessa forma, vai herdar tudo os testes e quando for para
# precisar fazer uma teste com fixture(dados para os testes) e so chamar essa funcoes
#make_caategory, make_recipe ou make_author
#agora usando o RecipeMixin para herdar todo
class RecipeTesteBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
    
        
        