import json

from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest


class LoginSerializer(Serializer):

    def from_json(self, content):
        data = json.loads(content)

        if "username" not in data:
            raise BadRequest("Username is required.")
        if "password" not in data:
            raise BadRequest("Password is required.")

        return data
