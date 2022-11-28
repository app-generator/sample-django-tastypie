from tastypie.resources import ModelResource

from api.authentication import JWTAuthentication
from api.user.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get']
        resource_name = 'auth/user'
        fields = ['username', 'email', 'password']
        authentication = JWTAuthentication()