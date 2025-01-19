from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authors.forms.recipe_form import AuthorRecipeForm

from recipes.models import Recipe

from .forms import RegisterForm, LoginForm


def register_view(request):
    register_form_data =  request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/resgister_view.html', {
        'form': form,
        'form_action' : reverse('authors:register_create'),
    })

#vai ler e validar o que o register_View manda e depois manda novamente para o register_view
def register_create(request):
    if not request.POST:  
        raise Http404()
    
    #ta salvando o dicionario do post inteiro ou seja os dados do form
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')

        # deletar a sessao depois de salva
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
    })



def login_create(request):
    if not request.POST:
        raise Http404()
    
    form  = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        #bem especifico
        if authenticated_user is not None:
            messages.success(request, 'You are logged in :)')
            login(request, authenticated_user)
        else:
            messages.error(request, 'INVALID CREDENTIALS')
    else:
        messages.error(request, 'INVALID USERNAME OR PASSWORD')

    return redirect(reverse('authors:dashboard'))


#essa view e fechada, o user tem que estar logado para funcionar
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request!!!')
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user!!!')
        return redirect(reverse('authors:login'))
    
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect(reverse('authors:login'))

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )


    return render(request, 'authors/pages/dashboard.html',{
        'recipes' : recipes,
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    # ele retorna uma query set, entao deve ter o first no final pra nao dar erro
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404()
    
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        #esse form e desse usuario
        recipe.author = request.user
        recipe.preparation_time_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Your Recipe is save successfully  :)')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))


    return render(request, 'authors/pages/dashboard_recipe.html',{
        'form': form
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_new(request):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe: Recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False

        recipe.save()

        messages.success(request, 'Salvo com sucesso!')
        return redirect(
            reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
        )

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context={
            'form': form,
            'form_action': reverse('authors:dashboard_recipe_new')
        }
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:  
        raise Http404()
    
    #ta salvando o dicionario do post inteiro ou seja os dados do form
    POST = request.POST
    id = POST.get('id')

    # ele retorna uma query set, entao deve ter o first no final pra nao dar erro
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id,
    ).first()

    if not recipe:
        raise Http404() 
    
    recipe.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect(reverse('authors:dashboard'))









