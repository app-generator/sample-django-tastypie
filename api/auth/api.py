from tastypie.resources import Resource
from tastypie import fields


class AuthenticationResource(Resource):

    username = fields.CharField()
    password = fields.CharField()

    class Meta:
        resource_name = 'auth'
