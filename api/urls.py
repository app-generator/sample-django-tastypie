from django.urls import path, include
from tastypie.api import Api

from api.auth.api import AuthenticationResource

api = Api(api_name='v1')

api.register(AuthenticationResource())

urlpatterns = [
    path('api', include(api.urls))
]
