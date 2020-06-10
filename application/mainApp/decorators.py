from .models import Pessoa
from users.models import CustomUser
from django.shortcuts import redirect, get_object_or_404

FORBIDDEN_URL = '/admin/'
STUDENTS = ['grad-cc', 'grad-si', 'grad-mc']
PROFS = ['prof']
"""
# Access restriction for user owner profile
def pessoa_owner_required(param):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            user = get_object_or_404(
                CustomUser,
                pk=kwargs[param]
            ).coordenador

            if request.user == user:
                return function(request, *args, **kwargs)
            else:
                return redirect('/')

        return wrap

    return decorator
"""
