from apps.common.utils.forms import FormModelBase
from apps.products.models import InventoryInput, Product


class InputMovementForm(FormModelBase):

    def __init__(self, *args, **kwargs):
        self.product_sku = kwargs.pop('product_sku',None)
        super().__init__(*args, **kwargs)

        if self.product_sku:
            product_qs = Product.objects.filter(sku=self.product_sku)
            self.fields['product'].queryset = product_qs
            if product_qs.exists():
                self.initial['product'] = product_qs.first()


    class Meta:
        model = InventoryInput
        fields = ['product', 'quantity','reference','notes']
        labels = {
            'product': 'Selecionar un producto',
            'quantity': 'Cantidad',
            'reference': 'Referencia de factura',
            'notes': 'Notas adicionales',
        }
