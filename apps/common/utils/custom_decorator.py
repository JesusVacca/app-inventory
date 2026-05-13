from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def redirect_authenticated_user(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('core:dashboard:dashboard')
    return wrapper

def role_required(roles:list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('core:accounts:login')
            if request.user.role not in roles:
                raise PermissionDenied
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
