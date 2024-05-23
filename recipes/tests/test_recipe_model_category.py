from .test_recipe_base import RecipeTesteBase
from django.core.exceptions import ValidationError


class RecipeCategoryModelTest(RecipeTesteBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()
    
    def test_recipe_category_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )
    
    def test_recipe_category_model_name_max_lenght_is_65_chairs(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
