from django.db import models


class Sale(models.Model):
    product = models.ForeignKey(
        "api_product.Product",
        on_delete=models.CASCADE,
        related_name='product_sales'
    )
    state = models.IntegerField()
    value = models.IntegerField()
    fee = models.IntegerField(default=0)
    client = models.CharField(max_length=128)
    currency = models.CharField(max_length=10, default="USD")
    payment_type = models.CharField(max_length=10, default="cc")
    purchase_date = models.DateTimeField(auto_now_add=True)
