from django.urls import path, include
app_name = 'core'
urlpatterns = [
    path('', include('apps.accounts.urls', namespace='accounts')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]