from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
import json


class LoginSerializer(Serializer):

    def from_json(self, content):
        if "username" not in content:
            raise BadRequest("Username is required.")
        if "password" not in content:
            raise BadRequest("Password is required.")

        return super().from_json(content)

    def to_json(self, data, options=None):
        print(data)
        return json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True)

    def deserialize(self, content, format='application/json'):
        print(content)
        return content
