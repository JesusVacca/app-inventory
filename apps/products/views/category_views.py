from apps.common.utils import role_required, RoleChoices
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.products.models import Category
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'categories'
    paginate_by = 10
    template_name = 'category/list.html'

    def get_queryset(self):
        return (
            Category.objects
            .annotate(count=Count('products'))
            .order_by('-count')
        )


@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('core:products:category-list')
    template_name = 'category/create.html'

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = '__all__'
    success_url = reverse_lazy('core:products:category-list')
    template_name = 'category/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_updated'] = True
        return context