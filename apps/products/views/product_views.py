from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.products.models import Product, Category
from apps.products.forms import ProductForm
from apps.common.utils import Notify, app_alerts, role_required, RoleChoices

"""
Clase que me permite listar productos
"""
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class ProductListView(LoginRequiredMixin, ListView):
    template_name = 'products/list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 20
    # Este metodo me permite mandar información a la vista de productos
    # Información como marca, categorías y alestar según el estado del producto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.__load_data())
        context['categories'] = Category.objects.all()
        params = self.request.GET.copy()
        params.pop('page', None)
        context['extra_param'] = params.urlencode()
        context['app_alerts'] = app_alerts()
        return context

    def get_queryset(self):
        qs = Product.objects.all().order_by('sku')
        dict_data = self.__load_data()
        search = dict_data.get('search')
        category_selected = dict_data.get('category_selected')

        if category_selected:
            qs = qs.filter(category_id=category_selected)
        if search:
            qs = qs.filter(name__icontains=search)
        return qs

    def __load_data(self):
        category_selected = self.request.GET.get('category_selected')
        try:
            category_selected = int(category_selected) if category_selected and category_selected.strip() != '' else 0
        except (ValueError, TypeError):
            category_selected = 0

        return {
            'search': self.request.GET.get('search', ''),
            'category_selected': category_selected
        }


"""
Esta clase me permite crear productos con ayuda de las clases genericas
'CreateView' -> Clase integrada de Django que me facilita lo previamente mencionado
"""
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('core:products:list')


"""
Clase que me ayuda actualizar información de producto
Apoyandome en las clases genericas del framework
"""
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class ProductUpdateView(UpdateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('core:products:list')
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    # Valida el objecto antes de ser creado
    # Además manda alertas al usuario de la acción que se realizo con ayuda de
    # la clase 'Notify'
    def form_valid(self, form):
        Notify.notify(
            request=self.request,
            message='Producto actualizado',
        )
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_updated'] = True
        return context