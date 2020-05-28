from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto, ProjetoIntegrante
from users.models import CustomUser
from .forms import ProjectEditForm, ProjectCreateForm, UserEditForm
from .decorators import teacher_required, project_owner_required
from django.contrib.auth.decorators import login_required

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


@login_required
def home(request):
    if request.user.title in ['prof', 'grad-cc', 'grad-si', 'grad-mc']:
        return redirect('/projectsApp/projects/')
    else:
        return redirect('/admin/')


def logout(request):
    logout(request)


# --------- TEACHER-ONLY STUFF ---------
@login_required
@teacher_required
@project_owner_required('pk')
def edit_project(request, pk):
    project = get_object_or_404(Projeto, pk=pk)

    members = project.projetointegrante_set.all().values_list('id', flat=True)
    non_members = CustomUser.objects.exclude(
                    projetointegrante__in=members
                  ).order_by('first_name', 'last_name', 'email')

    if request.method == "POST":
        form = ProjectEditForm(data=request.POST, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return redirect('/projectsApp/projects/')
    else:
        form = ProjectEditForm(instance=project)


    side_menu_items = SIDE_MENU_BASE
    context = {'project': project, 'form': form, 'non_members': non_members, 'menu': side_menu_items}

    return render(request, 'edit_project.html', context)


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
        form = ProjectCreateForm(data=request.POST, owner_pk=request.user.id)
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


# --------- PROFILE STUFF ---------

@login_required
def profile(request):
    side_menu_items = SIDE_MENU_BASE
    return render(request, 'home.html', {'menu': side_menu_items})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('/projectsApp/profile/')
    else:
        form = UserEditForm(
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': request.user.phone
            }
        )

    side_menu_items = SIDE_MENU_BASE

    return render(request, 'edit_profile.html',
                  {'form': form, 'menu': side_menu_items})


# --------- PROJECTS STUFF ---------

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
