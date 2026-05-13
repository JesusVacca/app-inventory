from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from apps.products.models import InventoryInput, InventoryOutput
from apps.products.forms import InputMovementForm, OutPutMovementForm
from apps.common.utils import Notify, role_required, RoleChoices

"""
    Entrada del inventario
"""
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class InputMovementView(ListView):
    model = InventoryInput
    template_name = 'inventory_movement/input_inventory_movement.html'
    context_object_name = 'input_movements'
    paginate_by = 20

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class CreateInputMovementView(CreateView):
    model = InventoryInput
    template_name = 'inventory_movement/create.html'
    success_url = reverse_lazy('core:products:inventory-input')
    form_class = InputMovementForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entrada de inventario'
        context['back_url'] = reverse('core:products:inventory-input')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        Notify.notify(
            request=self.request,
            message='Entrada registrada con exito!',
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product_sku'] = self.request.GET.get('product_sku',None)
        if kwargs.get('product_sku'):
            self.success_url = reverse_lazy('core:products:list')
        return kwargs


"""
    Salida de inventario
"""
@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class OutputMovementView(ListView):
    model = InventoryOutput
    template_name = 'inventory_movement/output_inventory.html'
    context_object_name = 'ouput_movements'
    paginate_by = 20

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class CreateOutputMovementView(CreateView):
    model = InventoryOutput
    template_name = 'inventory_movement/create.html'
    success_url = reverse_lazy('core:products:inventory-output')
    form_class = OutPutMovementForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Salida de inventario'
        context['back_url'] = reverse('core:products:inventory-output')
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        quantity = form.instance.quantity
        product = form.instance.product

        if quantity > product.stock:
            form.add_error('quantity', 'La cantidad no debe ser superior a las disponibles {}'.format(product.stock))
            return super().form_invalid(form)
        Notify.notify(
            request=self.request,
            message='Salida registrada con exito!',
        )
        return super().form_valid(form)
