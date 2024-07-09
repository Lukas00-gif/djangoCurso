from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='recipes-home'),
    path('recipes/search/', views.search , name='search'),
    path('recipes/category/<int:category_id>/', views.category, name='category'),
    path('recipes/<int:id>/', views.repice, name='recipe'),
]