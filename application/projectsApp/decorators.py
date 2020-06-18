from .models import Projeto, ProjetoIntegrante
from django.shortcuts import redirect, get_object_or_404

FORBIDDEN_URL = '/admin/'
STUDENTS = ['grad-cc', 'grad-si', 'grad-mc']
PROFS = ['prof']


# Builds decorators for access restrictions
def title_required(allowed_titles, fallback=FORBIDDEN_URL):
    def restriction_decorator(function):
        def wrap(request, *args, **kwargs):
            if request.user.title in allowed_titles:
                return function(request, *args, **kwargs)
            else:
                return redirect(fallback)

        return wrap

    return restriction_decorator


# Access restriction for student-only pages
def student_required(fun):
    return title_required(STUDENTS)(fun)


# Access restriction for teacher-only pages
def teacher_required(fun):
    return title_required(PROFS)(fun)


# Access restriction for project owner pages
def project_owner_required(param):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            coordenador = get_object_or_404(
                Projeto,
                pk=kwargs[param]
            ).coordenador

            if request.user == coordenador:
                return function(request, *args, **kwargs)
            else:
                return redirect('/')

        return wrap

    return decorator

# Access restriction for project owner pages
def project_owner_required_projetointegrante(param):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            coordenador = get_object_or_404(
                ProjetoIntegrante,
                pk=kwargs[param]
            ).projeto.coordenador

            if request.user == coordenador:
                return function(request, *args, **kwargs)
            else:
                return redirect('/')

        return wrap

    return decorator
