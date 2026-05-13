from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.accounts.models import Member
from apps.common.utils import Notify, role_required, RoleChoices
from apps.accounts.forms import MemberForm

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'accounts/list.html'
    context_object_name = 'members'


@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    template_name = 'accounts/create-member.html'
    success_url = reverse_lazy('core:accounts:member-list')
    form_class = MemberForm
    
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Usuario creado correctamente',
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
        

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'accounts/create-member.html'
    success_url = reverse_lazy('core:accounts:member-list')
    form_class = MemberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_updated'] = True
        return context

    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Usuario actualizado con exito',
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs