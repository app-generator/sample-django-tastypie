from tastypie.resources import ModelResource

from api.authentication import JWTAuthentication
from api.sale.models import Sale


class SaleResource(ModelResource):
    class Meta:
        queryset = Sale.objects.all()
        allowed_methods = ['get', "post"]
        resource_name = 'sales'
        fields = ['id', 'product', 'state', 'value', 'description', 'price', 'currency', 'date_created']
        authentication = JWTAuthentication()
