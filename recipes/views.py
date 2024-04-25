from django.shortcuts import render
from utils.recipes.factory import make_recipe

# estou importando o factory o make_recipe que cria basicamente
#varios nomes aleatorios para ajudar no preenchimento

def home(request):
    return render(request, 'recipes/pages/home.html', context={
        #esse recipes aki de baixo recebi a lista aleatoria gerada
        'recipes': [make_recipe() for _ in range(10)],
    })

def repice(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        #esse recipes aki de baixo, recebi somente um ja que em detailss e somente um
        #receita
        'recipe': make_recipe(),
        'is_detail_page': True
    })