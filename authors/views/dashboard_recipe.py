from django.views import View
from recipes.models import Recipe
from django.http.response import Http404
from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(
        login_url='authors:login', redirect_field_name='next'),
        name='dispatch')
class DashboardRecipe(View):
    def get_recipe(self, id):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id,
            ).first()

            if not recipe:
                raise Http404()
            
        return recipe
    

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html',{
            'form': form
        })


    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)


    def post(self, request, id=None):
        recipe = self.get_recipe(id)
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
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))
        
        return self.render_recipe(form)


@method_decorator(
    login_required(
        login_url='authors:login', redirect_field_name='next'),
        name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, request, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('authors:dashboard'))