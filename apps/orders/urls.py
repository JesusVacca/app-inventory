from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('select-product-per-order/', views.SelectProductsView.as_view(), name='select-product-per-order'),
    path('add-item-to-order/<int:pk>/', views.add_item_to_order, name='add-item-to-order'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete-order'),
    path('confirm-order/<int:pk>/', views.confirm_order, name='confirm-order'),

    path('sale-payments/', views.SalePaymentListView.as_view(), name='sale-payments'),
    path('sale-payments/create/', views.SalePaymentCreateView.as_view(), name='sale-payments-create'),

]