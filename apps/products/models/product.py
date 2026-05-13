from datetime import date, timedelta
from django.db import models
from apps.common.utils import generate_unique_sku

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )

    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=30, unique=True, editable=False, null=True, blank=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Precio compra
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Precio venta
    stock = models.PositiveIntegerField()
    stock_min = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock_value(self):
        return self.stock * self.price_sale

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_product_name_category'
            )
        ]


    @property
    def expired_product(self):
        if self.expiration_date and self.expiration_date < date.today():
            return True
        return False

    @property
    def expiration_status(self):
        current_date = date.today()
        if self.expiration_date:
            if  self.expiration_date >= current_date and self.expiration_date <= current_date + timedelta(days=5):
                return True
        return False

    def __str__(self):
        return f'{self.name}'

    def profit_margin(self):
        """Calcula el margen de ganancia en porcentaje."""
        if self.cost == 0:
            return None
        return round(((self.price - self.cost) / self.cost) * 100, 2)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)
        if not self.sku:
            self.sku = generate_unique_sku({
                'name': self.name[:6],
                'id': self.id,
            })
            super().save(update_fields=['sku'])

