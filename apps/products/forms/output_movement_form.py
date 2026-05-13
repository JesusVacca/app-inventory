from apps.common.utils.forms import FormModelBase
from apps.products.models import InventoryOutput

class OutPutMovementForm(FormModelBase):
    class Meta:
        model = InventoryOutput
        fields = ['product', 'quantity','reason','destination','notes']
        labels = {
            'product': 'Selecionar un producto',
            'quantity': 'Cantidad',
            'reason': 'Motivo',
            'destination': 'Destino',
            'notes': 'Notas adicionales',
        }
