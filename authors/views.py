from django.shortcuts import render



def register_view(request):
    return render(request, 'authors/pages/resgister_view.html')
