from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Recipe

# estou importando o factory o make_recipe que cria basicamente
#varios nomes aleatorios para ajudar no preenchimento

def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
        ).order_by('-id')
    
    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 5)
    page_obj = paginator.get_page(current_page)


    return render(request, 'recipes/pages/home.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': page_obj,
    })

def category(request, category_id):
    #pedindo para filtrar atravez do category_id
    # e so colocar o __ sendo q e uma forenkey = ao valor q eu quiser no caso category_id
    #esse getlistor 404 e uma funçao que vai retornar uma lista e se n tiver retorar o erro 404
    #precisa passar o model e os filtros logo depois
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': recipes,
        'title': f'{recipes[0].category.name}'
    })

def repice(request, id):
    # recipe = Recipe.objects.get(id=id)
    # recipe = Recipe.objects.filter(
    #     id=id,
    #     is_published=True,
    # ).order_by('-id').first()

    # do msm jeito da anterior, mais aqui e pega um unico objeto(tem q ter id) ou da erro 404
    recipe = get_object_or_404(Recipe, id=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', context={
        #esse recipes aki de baixo, recebi somente um ja que em detailss e somente um
        #receita
        # 'recipe': make_recipe(),
        'recipe': recipe,
        'is_detail_page': True
    })

def search(resquest):
    search_term = resquest.GET.get('q', '').strip()
    
    if not search_term:
        raise Http404
    
    recipes = Recipe.objects.filter(
        #quero todas as receitas q contenha o texto q esta ali no texto
        # depentimente de ser maiuscula ou minuscula
        # O Q representa a mudança para o OR de vez de AND usando o | 
        Q(
            Q(title__icontains = search_term) | 
            Q(description__icontains = search_term),
        )
    ).order_by('-id')

    return render(resquest, 'recipes/pages/search.html', {
        'page_title': f'Search for { search_term } |',
        'search_term' : search_term,
        'recipes' : recipes,
    })