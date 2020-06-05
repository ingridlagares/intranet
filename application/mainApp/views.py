from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from projectsApp.models import Projeto, ProjetoIntegrante, ProjetoArea
from .models import Area
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomepageManage(View):

    def get(self, request):
        return redirect('/projectsApp/projects/')
