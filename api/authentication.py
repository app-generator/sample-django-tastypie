import jwt
from django.conf import settings
from tastypie.authentication import Authentication
from tastypie.exceptions import BadRequest

from api.user.models import User


class PassAuthentication(Authentication):
    """Authentication class which allows some services to all users (logged-in/logged-out)"""

    def is_authenticated(self, request, **kwargs):
        return True


class JWTAuthentication(Authentication):

    def _authenticate_credentials(self, token):

        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = {"success": False, "msg": "Invalid authentication. Could not decode token."}
            raise BadRequest(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = {"success": False, "msg": "No user matching this token was found."}
            raise BadRequest(msg)

        if not user.is_active:
            msg = {"success": False, "msg": "This user has been deactivated."}
            raise BadRequest(msg)

        return user, token
