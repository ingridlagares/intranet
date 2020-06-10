from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from projectsApp.models import Projeto, ProjetoIntegrante, ProjetoArea
from .models import Area, Pessoa
from .forms import PessoaEditForm
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DetailView, ListView, TemplateView,
                                  UpdateView)

SIDE_MENU_BASE = [
    {
        "name": "Meus projetos",
        "icon": "assignment",
        "href": 'projects'
    },
    {
        "name": "Meu perfil",
        "icon": "account_circle",
        "href": 'profile'
    }
]

class HomepageManage(View):
    def get(self, request):
        return redirect('/projectsApp/projects/')

pessoa_decorator = [login_required]
@method_decorator(pessoa_decorator, name='dispatch')
class pessoaEditView(UpdateView):
    model = Pessoa
    template_name = 'edit_profile.html'
    form_class = PessoaEditForm
    success_url = '/projectsApp/profile/'
    context_object_name = 'pessoa'
    extra_context={'menu': SIDE_MENU_BASE}

#    def get_queryset(self):
#        return self.Pessoa.filter(user=request.user)

@login_required
def profile(request):
    side_menu_items = SIDE_MENU_BASE
    user =  request.user
    pessoa =  Pessoa.objects.get(user=user)
    return render(request, 'home.html', {'menu': side_menu_items, 'pessoa': pessoa})
