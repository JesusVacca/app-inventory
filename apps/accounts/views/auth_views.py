from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View


from apps.common.utils import Notify, redirect_authenticated_user


@method_decorator(redirect_authenticated_user, name='dispatch')
class LoginView(LoginView):
    template_name = 'accounts/login.html'
    def form_invalid(self, form):
        for error_list in form.errors.values():
            Notify.notify(
                request=self.request,
                message=error_list[0],
                level='error',
            )
        return super().form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

