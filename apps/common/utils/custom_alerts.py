from django.db.models import F, Count
from datetime import date, timedelta
from apps.products.models import Product

def app_alerts():
    list_map = []

    current_date = date.today()
    deadline = current_date + timedelta(days=5)

    # Productos con stock bajo
    low_stock = Product.objects.filter(stock__lte=F('stock_min'))

    if low_stock.exists():
        list_map.append({
            'level': 'warning',
            'message': f'Hay {low_stock.count()} producto(s) con stock bajo',
            'icon': 'bi bi-exclamation-triangle',
        })



    return list_map