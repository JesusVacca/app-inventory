from django.db.models import TextChoices

class RoleChoices(TextChoices):
    Admin = ('Admin', 'Admin',)
    Cliente = ('Cliente', 'Cliente',)
    Vendedor = ('Vendedor', 'Vendedor',)
    Repartidor = ('Repartidor', 'Repartidor',)



class UnitOfMeasure(TextChoices):
    UNIDAD = 'UN', 'Unidades'
    KILOGRAMO = 'KG', 'Kilogramos'
    LIBRA = 'LB', 'Libras'
    LITRO = 'LT', 'Litros'
    CAJA = 'BX', 'Cajas'
    PAQUETE = 'PK', 'Paquetes'
    METRO = 'M', 'Metros'
    CENTIMETRO = 'CM', 'Centímetros'


class OutputReason(TextChoices):
    TRANSFER = 'Transferencia entre sucursales', 'Transferencia entre sucursales'
    ASSIGNMENT = 'Asignación a empleados', 'Asignación a empleados'
    RETURN = 'Devolución a proveedor', 'Devolución a proveedor'
    DEFECT = 'Producto defectuoso', 'Producto defectuoso'
    DONATION = 'Donación', 'Donación'
    OTHER = 'Otro', 'Otro'


class OrderStatus(TextChoices):
    PENDING = 'Pendiente', 'Pendiente'
    PAID = 'Pagada', 'Pagada'
    CREDIT = 'Crédito', 'Crédito'
    CANCELLED = 'Cancelada', 'Cancelada'
    RETURNED = 'Devuelta', 'Devuelta'

class PaymentMethod(TextChoices):
    CASH = 'Efectivo', 'Efectivo'
    TRANSFER = 'Transferencia', 'Transferencia'
    CREDIT = 'Credito', 'Crédito'
