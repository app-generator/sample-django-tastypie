from django.urls import path, include
from tastypie.api import Api

from api.auth.api import AuthenticationResource
from api.user.api import UserResource

api = Api(api_name='v1')

api.register(AuthenticationResource())
api.register(UserResource())

urlpatterns = [
    path('api/', include(api.urls))
]
