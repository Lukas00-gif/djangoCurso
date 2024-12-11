from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    request.session['register_for_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your user is created, please log in')

        #deletar a sessao depois de salva
        del(request.session['register_for_data'])
        return redirect(reverse('authors:login'))

    return redirect('authors:register')

    # return render(request, 'authors/pages/resgister_view.html', {
    #     'form': form,
    # })

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
    login_url = reverse('authors:login')

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

    return redirect(login_url)

#essa view e fechada, o user tem que estar logado para funcionar
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))
    
    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))
    
    logout(request)
    return redirect(reverse('authors:login'))



