from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from apps.orders.forms import SalePaymentForm
from apps.orders.models import Order, SalePayment
from apps.common.utils import PaymentMethod, OrderStatus, Notify, role_required, RoleChoices


@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class SalePaymentListView(ListView):
    model = SalePayment
    context_object_name = 'sale_payments'
    template_name = 'sale_payment/list.html'

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class SalePaymentCreateView(CreateView):
    model = SalePayment
    success_url = reverse_lazy('core:orders:sale-payments')
    form_class = SalePaymentForm
    template_name = 'sale_payment/create.html'
    def form_valid(self, form):
        amount = form.instance.amount
        order = form.instance.sale
        form.instance.customer = order.customer
        if amount < 0:
            form.add_error(
                'amount',
                f'La cantidad a abonar debe ser superior a 1000 (actual: {amount})'
            )
            return self.form_invalid(form)

        if order.payment_method == PaymentMethod.CREDIT:
            total = order.total
            if amount > total:
                form.add_error(
                    'amount',
                    f'La cantidad a abonar debe ser inferior o igual a la deuda {total} (actual: {amount})'
                )
                return self.form_invalid(form)
            total -= amount
            form.instance.sale.total = total
            form.instance.sale.save(update_fields=['total'])
            if total <= 0:
                form.instance.sale.status = OrderStatus.PAID
                form.instance.sale.save(update_fields=['status'])
        Notify.notify(
            self.request,
            'Abono aprovado con exito'
        )
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order_id'] = self.request.GET.get('sale-id')
        return kwargs

