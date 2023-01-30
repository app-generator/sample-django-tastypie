from django.contrib import admin
from api.sale.models import Sale
from api.product.models import Product

admin.site.register(Sale)
admin.site.register(Product)