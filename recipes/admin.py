# admin senha 123456

from django.contrib import admin
from . models import Category, Recipe

class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published')
    list_display_links = ['title']
    search_fields = ('id', 'title', 'description', 'slug', 'preparation_steps')
    list_filter = ('category', 'author', 'is_published', 'preparation_step_is_html')
    list_per_page = 10
    list_editable = ['is_published']
    ordering = ['-id']
    prepopulated_fields = {"slug": ['title']}

admin.site.register(Category, CategoryAdmin)

