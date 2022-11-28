from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.urls import re_path
from tastypie import fields
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource

from api.auth.serializers import LoginSerializer
from api.authentication import PassAuthentication
from api.user.api import UserResource
from api.user.models import User


def _generate_jwt_token(user):
    token = jwt.encode(
        {"id": user.pk, "exp": datetime.utcnow() + timedelta(days=7)},
        settings.SECRET_KEY,
    )

    return token


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
            re_path(r"login", self.wrap_view('login'), name="api_login"),
        ]

    def login(self, request, **kwargs):
        """
        Function for providing the login api endpoint.
        """
        self.method_check(request, allowed=['post'])

        serializer = LoginSerializer()

        data = serializer.from_json(request.body)

        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise BadRequest({"success": False, "msg": "Wrong credentials"})

        if not user.is_active:
            raise BadRequest(
                {"success": False, "msg": "User is not active"}
            )

        return self.create_response(request, {
            "success": True,
            "token": _generate_jwt_token(user),
            "user": {"id": user.pk, "username": user.username, "email": user.email},
        })
