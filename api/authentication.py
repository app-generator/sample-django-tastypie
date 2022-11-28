import jwt
from django.conf import settings
from tastypie.authentication import Authentication
from tastypie.exceptions import BadRequest

from api.user.models import User


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, str):
        # Work around django test client oddness
        auth = auth.encode('iso-8859-1')
    return auth


class PassAuthentication(Authentication):
    """Authentication class which allows some services to all users (logged-in/logged-out)"""

    def is_authenticated(self, request, **kwargs):
        return True


class JWTAuthentication(Authentication):

    def is_authenticated(self, request, **kwargs):
        request.user = None

        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        token = auth_header.decode("utf-8")

        user, _ = self._authenticate_credentials(token)
        if user:
            return True

        return False

    def get_identifier(self, request):
        return request.user

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
