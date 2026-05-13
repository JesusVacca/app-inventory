from django.db import models
from apps.common.utils.choices import OutputReason

class InventoryMovementBase(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True



class InventoryInput(InventoryMovementBase):
    reference = models.CharField(max_length=100, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.pk: return
        if self.quantity > 0:
            self.product.stock += self.quantity
            self.product.save(update_fields=['stock'])

        super().save(*args, **kwargs)

class InventoryOutput(InventoryMovementBase):
    reason = models.CharField(
        choices=OutputReason.choices,
        max_length=100,
        default=OutputReason.OTHER,
    )
    destination = models.CharField(max_length=100, blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.pk: return
        if self.quantity <= self.product.stock:
            self.product.stock -= self.quantity
            self.product.save(update_fields=['stock'])
        super().save(*args, **kwargs)