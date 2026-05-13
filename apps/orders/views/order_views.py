from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime, timedelta
from django.db import IntegrityError, transaction
from django.db.models import Sum, Q

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, TemplateView

from apps.orders.models import Order, OrderItem
from apps.products.models import Product
from apps.orders.forms import OrderForm
from apps.common.utils import Notify, OrderStatus, PaymentMethod, role_required, RoleChoices


@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_end'] = self.request.GET.get('date_end',None)
        context['date_start'] = self.request.GET.get('date_start',None)
        context['search'] = self.request.GET.get('search','')
        context['status'] = self.request.GET.get('status','')
        context['arrears'] = self.request.GET.get('arrears',None)
        context['order_status'] = OrderStatus
        return context

    def get_queryset(self):
        date_format = "%Y-%m-%d"
        queryset = Order.objects.all()
        date_end = self.request.GET.get('date_end',None)
        date_start = self.request.GET.get('date_start',None)
        search = self.request.GET.get('search','')
        status = self.request.GET.get('status','')
        arrears = self.request.GET.get('arrears',None)

        if arrears == '1':
            queryset = queryset.filter(
                status=OrderStatus.PENDING,
                deadline_date__lt=timezone.now().date(),
            )

        if arrears == '0':
            queryset = queryset.filter(
                Q(status=OrderStatus.PAID) |
                Q(deadline_date__gte=timezone.now().date())
            )

        if search:
            queryset = queryset.filter(
                Q(customer__first_name__icontains=search)
                | Q(customer__email__icontains=search)
                | Q(customer__phone_number__icontains=search)
            )

        if date_start:
            date_start = datetime.strptime(date_start, date_format)
            queryset = queryset.filter(created_at__gte=date_start)

        if date_end:
            date_end = datetime.strptime(date_end, date_format)
            queryset = queryset.filter(created_at__lte=date_end + timedelta(days=1))

        if status:
            queryset = queryset.filter(status=status)

        return queryset

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create-order.html'
    success_url = reverse_lazy('core:orders:select-product-per-order')
    def form_valid(self, form):
        order = form.save()
        self.request.session['order_id'] = order.id
        return super().form_valid(form)

@method_decorator(role_required([RoleChoices.Admin, RoleChoices.Vendedor]), name='dispatch')
class SelectProductsView(ListView):
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    template_name = 'orders/select-product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.request.session.get('order_id')
        order = Order.objects.filter(id=order_id).first()
        context['total'] = order.total_to_pay
        context['order'] = order
        context['search'] = self.request.GET.get('search','')


        return context

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gt=0).order_by('-id')
        search = self.request.GET.get('search','')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

@role_required([RoleChoices.Admin, RoleChoices.Vendedor])
def confirm_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.total = order.total_to_pay
    order.save(update_fields=['total'])
    if order.items.exists():
        for item in order.items.all():
            product = item.product
            stock = item.quantity
            product.stock -= stock
            product.save(update_fields=['stock'])
        if order.payment_method == PaymentMethod.CASH:
            order.status = OrderStatus.PAID
            order.save(update_fields=['status'])
    return HttpResponseRedirect(reverse_lazy('core:orders:list'))

@role_required([RoleChoices.Admin, RoleChoices.Vendedor])
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.total > 0 and order.items.exists():
        Notify.notify(
            request,
            'No es posible eliminar esta venta',
            'info'
        )
    else:
        order.items.all().delete()
        order.delete()
        Notify.notify(
            request,
            'Venta eliminada con exito',
        )
    return HttpResponseRedirect(reverse_lazy('core:orders:list'))

@role_required([RoleChoices.Admin, RoleChoices.Vendedor])
def add_item_to_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    product_sku = request.POST.get('product_sku')
    amount = int(request.POST.get('amount'))
    product = get_object_or_404(Product, sku=product_sku)
    url = request.path


    with transaction.atomic():
        item, created = OrderItem.objects.get_or_create(
            product=product,
            order=order,
            defaults={
                'quantity': amount
            }
        )
        if not created:
            item.quantity = amount
            item.save()

    Notify.notify(
        request,
        'Producto agregado con exito',
    )

    return HttpResponseRedirect(reverse_lazy('core:orders:select-product-per-order'))
