from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404
from django.contrib import messages
from django.urls import reverse 



def register_view(request):
    register_form_data =  request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
        
    return render(request, 'authors/pages/resgister_view.html', {
        'form': form,
        'form_action' : reverse('authors:create'),
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

    return redirect('authors:register')

    # return render(request, 'authors/pages/resgister_view.html', {
    #     'form': form,
    # })
