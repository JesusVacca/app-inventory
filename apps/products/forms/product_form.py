from datetime import date
from django import forms
from apps.products.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'stock_min',
            'stock',
            'price',
            'price_sale',
            'image',
            'description',
        ]
        labels = {
            'name':'Nombre del producto',
            'category':'Selecionar categoría',
            'stock':'Stock maximo',
            'stock_min':'Stock minimo',
            'price':'Precio de compra',
            'price_sale':'Precio de venta',
            'description':'Descripción del producto',
            'image':'Selecionar Imagen del producto',
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['stock'].disabled = True

    def clean(self):
        clean_data = super().clean()
        stock = clean_data.get('stock')
        stock_min = clean_data.get('stock_min')

        name = clean_data.get('name').title()
        brand = clean_data.get('brand')
        category = clean_data.get('category')



        if name and brand and category:
            qs = Product.objects.filter(name=name, brand=brand, category=category)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error('name', f'Ya existe un producto con esa marca y categoría')

        if stock_min:
            if stock < stock_min and not self.instance:
                self.add_error('stock','El stock no debe ser menor que el stock mínimo')
        return clean_data