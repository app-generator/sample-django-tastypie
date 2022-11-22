from tastypie.resources import Resource


class AuthenticationResource(Resource):

    class Meta:
        resource_name = 'auth'