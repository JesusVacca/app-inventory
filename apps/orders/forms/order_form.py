from datetime import date
from django import forms
from apps.common.utils import FormModelBase
from apps.orders.models import Order


class OrderForm(FormModelBase):
    class Meta:
        model = Order
        fields = ['customer','phone_number','payment_method','interest_rate','deadline_date']
        labels = {
            'customer':'Selecionar cliente',
            'phone_number':'Número de telefono del cliente',
            'payment_method':'Selecionar metodo de pago',
            'interest_rate':'Intereses (%)',
            'deadline_date':'Plazo a pagar',
        }
        widgets = {
            'deadline_date':forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': date.today().strftime('%Y-%m-%d'),
                },
                format='%Y-%m-%d',
            ),
        }
