from django.utils import timezone

from django.db import models
from apps.common.utils import PaymentMethod, OrderStatus

class Order(models.Model):
    customer = models.ForeignKey(
        'accounts.Member',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    payment_method = models.CharField(
        max_length=13,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH
    )
    status = models.CharField(
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        max_length=10
    )
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_in_arrears(self):
        if self.deadline_date:
            return self.deadline_date < timezone.now() and self.status == OrderStatus.PENDING
        return False

    @property
    def total_to_pay(self):
        if self.items.exists():
            total = sum([item.subtotal for item in self.items.all()])
            return (total * self.interest_rate/100) + total
        return 0

    def __assignament_customer(self):
        if self.customer:
            return self.customer
        if self.phone_number:
            from apps.accounts.models import Member
            customer, _ = Member.objects.get_or_create(
                phone_number=self.phone_number,
                defaults={
                    'first_name': 'Defaul name',
                    'last_name': 'Defaul last name',
                    'email': 'customer_{}@example.com'.format(self.phone_number),
                }
            )
            return customer
        return None

    def __str__(self):
        return f'Order #{self.id} - {self.customer} - {self.payment_method} - {self.total}'

    def save(self, *args, **kwargs):
        if not self.customer:
            self.customer = self.__assignament_customer()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name='items')
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    @property
    def subtotal(self):
        return self.quantity * self.product.price_sale

    def __str__(self):
        return f'{self.order} - {self.quantity}'
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'product'],
                name='unique_order_item'
            )
        ]


