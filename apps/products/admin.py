from django.contrib import admin
from apps.products.models import Product, Category, InventoryInput, InventoryOutput
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(InventoryInput)
admin.site.register(InventoryOutput)
