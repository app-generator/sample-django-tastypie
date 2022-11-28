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

        auth_header = get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != 'bearer':
            return None

        user, _ = self._authenticate_credentials(token)
        if user:
            return True

        return False

    def get_identifier(self, request):
        return request.user

    def _authenticate_credentials(self, token):
        print(token)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
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
