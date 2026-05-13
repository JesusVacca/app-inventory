from apps.common.utils import PaymentMethod, OrderStatus
from django.db import models

class SalePayment(models.Model):

    class _PaymentMethod(models.TextChoices):
        CASH = 'Efectivo','Efectivo'

    sale = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='payments',
    )
    customer = models.ForeignKey('accounts.Member', on_delete=models.CASCADE, related_name='payments', editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=10,
        choices=_PaymentMethod.choices,
        default=_PaymentMethod.CASH,
    )
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

