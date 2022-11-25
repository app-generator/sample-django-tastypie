from tastypie.authentication import Authentication


class PassAuthentication(Authentication):
    """Authentication class which allows some services to all users (logged-in/logged-out)"""

    def is_authenticated(self, request, **kwargs):
        return True
