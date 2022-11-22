from tastypie.authentication import BasicAuthentication
from tastypie.resources import ModelResource

from api.user.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        authentication = BasicAuthentication()