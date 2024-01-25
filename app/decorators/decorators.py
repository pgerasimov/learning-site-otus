from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def student_required(view_func):
    actual_decorator = login_required(lambda u: u.is_authenticated and hasattr(u, 'userprofile') and u.userprofile.role == 'student')
    return actual_decorator


def teacher_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request, 'user') and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        print(request.user.is_authenticated)
        print(hasattr(request.user, 'userprofile'))
        print(request.user.userprofile.role)
        if hasattr(request, 'user') and request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")
    return _wrapped_view



