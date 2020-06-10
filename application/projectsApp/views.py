from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto, ProjetoIntegrante, ProjetoArea
from mainApp.models import Area
from users.models import CustomUser
from .forms import ProjectEditForm, ProjectCreateForm
from .decorators import teacher_required, project_owner_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.views import LogoutView
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

teacher_decorator = [project_owner_required('pk'), teacher_required, login_required]
@method_decorator(teacher_decorator, name='dispatch')
class projectEditView(UpdateView):
    model = Projeto
    template_name = 'edit_project.html'
    form_class = ProjectEditForm
    success_url = '/projectsApp/projects/'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        members = project.projetointegrante_set.all().values_list('id', flat=True)
        non_members = CustomUser.objects.exclude(
                    projetointegrante__in=members
                  ).order_by('first_name', 'last_name', 'email')
        side_menu_items = SIDE_MENU_BASE
        context['project'] = project
        context['menu'] = side_menu_items
        context['non_members'] = non_members
        return context

@login_required
@teacher_required
@project_owner_required('pk')
def delete_project(request, pk):
    project = get_object_or_404(Projeto, pk=pk)
    project.delete()

    return redirect('/projectsApp/projects/')


@login_required
@teacher_required
def create_project(request):
    if request.method == "POST":
        form = ProjectCreateForm(request.POST, request.FILES, owner_pk = request.user.id)
        if form.is_valid():
            project_members = form.cleaned_data['project_members']
            project = form.save(commit=False)
            project.coordenador = request.user
            project.save()

            # add selected new members
            for new_member in project_members:
                ProjetoIntegrante.objects.create(
                    integrante=new_member,
                    projeto=project
                )

            # add the project owner as a member since it was not included
            # in the list
            ProjetoIntegrante.objects.create(
                integrante=request.user,
                projeto=project
            )

            return redirect('/projectsApp/projects/')
    else:
        form = ProjectCreateForm(owner_pk=request.user.id)

    side_menu_items = SIDE_MENU_BASE
    context = {'form': form, 'menu': side_menu_items}

    return render(request, 'create_project.html', context)


@login_required
@teacher_required
@project_owner_required('project_pk')
def delete_project_member(request, project_pk, member_pk):
    member = ProjetoIntegrante.objects.filter(integrante=member_pk,
                                              projeto=project_pk)[0]
    member.delete()

    return redirect('/projectsApp/projects/%d/edit' % project_pk)


@login_required
@teacher_required
@project_owner_required('project_pk')
def add_selected_member(request, project_pk):
    nonmember_pk = request.POST.get('non_members', None)
    return redirect(
        '/projectsApp/projects/%d/add_project_member/%s' % (project_pk, nonmember_pk)
    )


@login_required
@teacher_required
@project_owner_required('project_pk')
def add_project_member(request, project_pk, member_pk):
    integrante = get_object_or_404(CustomUser, pk=member_pk)
    projeto = get_object_or_404(Projeto, pk=project_pk)
    ProjetoIntegrante.objects.create(
        integrante=integrante, projeto=projeto
    )

    return redirect('/projectsApp/projects/%d/edit' % project_pk)

# --------- PROJECTS STUFF ---------#

@login_required
def projects(request):
    user_projects = list(Projeto.objects.filter(coordenador=request.user.id))
    projects_user_is_in = list(map(
        lambda x: x.projeto,
        ProjetoIntegrante.objects.filter(integrante=request.user.id)
    ))
    if request.user.title == 'prof':
        isTeacher = True;
    else:
        isTeacher = False;

    projects = set(user_projects + projects_user_is_in)

    side_menu_items = SIDE_MENU_BASE

    return render(request, 'projects.html', {
        'projects': projects,
        'menu': side_menu_items,
        'isTeacher': isTeacher
    })
