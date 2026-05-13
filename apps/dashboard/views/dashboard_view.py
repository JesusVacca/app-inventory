from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum, Count
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.common.utils import OrderStatus, role_required,RoleChoices
from apps.accounts.models import Member


@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'


    def __map(self, title='', icon='bi bi-check', count=0, text_aux='', class_element=''):
        return {
            'title': title,
            'icon': icon,
            'count': count,
            'text_aux': text_aux,
            'class': class_element
        }


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        LIST_INFO_MAP = []

        counter_product = Product.objects.all().count()
        counter_member = Member.objects.all().count()

        low_stock = Product.objects.filter(
            stock__lte=F('stock_min')
        )
        total_inventory_value = Product.objects.aggregate(
            total=Sum(F('price') * F('stock'))
        )['total'] or 0

        sale_pending = Order.objects.filter(status=OrderStatus.PENDING).aggregate(
            total=Sum(F('total'))
        )

        # Productos más vendidos

        top_products = (
            OrderItem.objects
            .values('product_id', 'product__name')
            .annotate(total_sold=Sum('quantity'))
        )

        if sale_pending.get('total'):
            LIST_INFO_MAP.append(self.__map(
                title='Valor ventas pendientes',
                icon='bi bi-coin',
                count=f'{sale_pending['total']:,.2f}'.replace('.','X').replace(',','.').replace('X',','),
                text_aux='Valor ventas pendientes (COP)',
            ))

        if counter_member:
            LIST_INFO_MAP.append(self.__map(title='Usuarios',icon='bi bi-people',count=counter_member,text_aux='Usuarios registrados'))
        if total_inventory_value:
            LIST_INFO_MAP.append(self.__map(
                title='Valor inventario (COP)',
                icon='bi bi-coin',
                count=f'{total_inventory_value:,.2f}'.replace('.','X').replace(',','.').replace('X',','),
                text_aux='Valor inventario (COP)',
                class_element='info'
            ))

        if counter_product > 0:
            LIST_INFO_MAP.append(
                self.__map(
                    title='Total de productos',
                    icon='bi bi-boxes',
                    count=counter_product,
                    text_aux='En inventario',
                )
            )

        if low_stock.exists():
            LIST_INFO_MAP.append(
                self.__map(
                    title='Stock bajo',
                    icon='bi bi-exclamation-triangle',
                    count=low_stock.count(),
                    text_aux='Requieren atención',
                    class_element='danger'
                )
            )

        context['LIST_INFO_MAP'] = LIST_INFO_MAP
        context['low_stock'] = low_stock[:10]
        context['top_products'] = top_products[:10]
        return context
