from django.contrib.auth import authenticate
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource
from tastypie import fields

from api.authentication import PassAuthentication
from api.user.api import UserResource
from api.user.models import User
from django.urls import path


class AuthenticationResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=False)

    class Meta:
        resource_name = 'auth'
        queryset = User.objects.all()
        authentication = PassAuthentication()
        allowed_methods = ['post']
        include_resource_uri = False

    def obj_create(self, bundle, **kwargs):
        """Overrides the obj_create method of ModelResource"""
        user_data = bundle.data.get("user")
        if user_data is None:
            raise BadRequest("User data is required.")
        try:
            User.objects.get(username=user_data['username'])
            raise BadRequest("An user with this username already exists.")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data['password']
            )
            bundle.obj = self._meta.object_class()
            return user

    def prepend_urls(self):
        """Appending urls after profile resource for login and logout."""
        return [
            path("login", self.wrap_view('login'), name="api_login"),
        ]

    def login(self, request, **kwargs):
        """
        Function for providing the login api endpoint.
        """
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get(
            'CONTENT_TYPE', 'application/json'))
        username = data.pop('username')
        password = data.pop('password')
        user = authenticate(username=username, password=password)
        if user:
            return {
                "good": "good"
            }
