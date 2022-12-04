from tastypie.resources import ModelResource

from api.authentication import JWTAuthentication
from api.product.models import Product


class ProductResource(ModelResource):
    class Meta:
        queryset = Product.objects.all()
        allowed_methods = ['get', "post"]
        resource_name = 'product'
        fields = ['id', 'user_id', 'name', 'information', 'description', 'price', 'currency', 'date_created']
        authentication = JWTAuthentication()
