
from apps.common.utils import FormModelBase, OrderStatus
from apps.orders.models import SalePayment, Order


class SalePaymentForm(FormModelBase):

    def __init__(self, *args, **kwargs):
        self.order_id = kwargs.pop('order_id', None)
        super().__init__(*args, **kwargs)

        self.fields['sale'].queryset = Order.objects.filter(status=OrderStatus.PENDING)
        if self.order_id:
            self.fields['sale'].queryset = Order.objects.filter(id=self.order_id)


    class Meta:
        model = SalePayment
        fields = ['sale', 'amount', 'payment_method','notes']
        labels = {
            'sale':'Selecionar venta',
            'amount':'Cantidad (Pesos)',
            'payment_method':'Metodos de pago',
            'notes':'Notas adicionales',
        }
