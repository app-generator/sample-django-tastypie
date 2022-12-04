from django.db import models


class Product(models.Model):
    user_id = models.IntegerField(default=1)
    name = models.CharField(max_length=128)
    information = models.CharField(max_length=128)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=10, default="USD")
    date_created = models.DateTimeField(auto_now_add=True)
