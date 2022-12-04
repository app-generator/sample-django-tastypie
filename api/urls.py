from django.urls import path, include
from tastypie.api import Api

from api.auth.api import AuthenticationResource
from api.user.api import UserResource
from api.product.api import ProductResource
from api.sale.api import SaleResource

api = Api(api_name='v1')

api.register(AuthenticationResource())
api.register(UserResource())
api.register(ProductResource())
api.register(SaleResource())

urlpatterns = [
    path('api/', include(api.urls))
]
