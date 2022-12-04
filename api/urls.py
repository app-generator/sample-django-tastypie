from django.urls import path, include
from tastypie.api import Api

from api.auth.api import AuthenticationResource
from api.user.api import UserResource
from api.product.api import ProductResource

api = Api(api_name='v1')

api.register(AuthenticationResource())
api.register(UserResource())
api.register(ProductResource())

urlpatterns = [
    path('api/', include(api.urls))
]
