from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=20)
    servings = models.CharField(max_length=20)
    servings_unit = models.CharField(max_length=20)
    preparation_step = models.TextField()
    preparation_step_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d')

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='category', blank=True, default=None)
    
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        related_name='author', blank=True)

    def __str__(self):
        return self.title    

