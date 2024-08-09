from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q

from utils.pagination import make_pagination
from .models import Recipe

import os

# estou importando o factory o make_recipe que cria basicamente
#varios nomes aleatorios para ajudar no preenchimento


PER_PAGE = int(os.environ.get('PER_PAGE', 3))


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True,
        ).order_by('-id')
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)


    return render(request, 'recipes/pages/home.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': page_obj,
        'pagination_range': pagination_range
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
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': page_obj,
        'pagination_range': pagination_range,
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

def search(request):
    search_term = request.GET.get('q', '').strip()
    
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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'Search for { search_term } |',
        'search_term' : search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
    })