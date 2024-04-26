from django.shortcuts import render
from utils.recipes.factory import make_recipe

from .models import Recipe

# estou importando o factory o make_recipe que cria basicamente
#varios nomes aleatorios para ajudar no preenchimento

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
        ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': recipes,
    })

def category(request, category_id):
    #pedindo para filtrar atravez do category_id
    # e so colocar o __ sendo q e uma forenkey = ao valor q eu quiser no caso category_id
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True,
        ).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': recipes,
    })

def repice(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        #esse recipes aki de baixo, recebi somente um ja que em detailss e somente um
        #receita
        'recipe': make_recipe(),
        'is_detail_page': True
    })