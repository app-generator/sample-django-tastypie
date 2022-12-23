
# Django TastyPie Pros and Cons 

Django TastyPie is a web service API framework for Django providing tools and utils to create REST API interfaces. It can be a great alternative to the Django REST framework if you are looking for a simple micro-framework to plug into your Django project. In this article, we will quickly talk about the pros and cons of Django TastyPie.

## Pros

Tastypie was built with simplicity in its architecture and utils. With Django TastyPie, you can have pros such as:

* A set of default behaviors: Using TastyPie `Resource` class, for example, you can quickly create an endpoint that can be accessed from an URL. For example, let's say we are creating an endpoint to retrieve `products` from an URL.

    ```python
    class ProductResource(ModelResource):
        class Meta:
            queryset = Product.objects.all()
            allowed_methods = ['get', "post", "delete", "put"]
            resource_name = 'products'
            fields = ['id', 'user_id', 'name', 'information', 'description', 'price', 'currency', 'date_created']
            validation = FormValidation(form_class=ProductForm)
    ```

    And you just need to register this new resource with the version of the API in the `urls.py`.

    ```python
    from tastypie.api import Api
    from api.product.api import ProductResource
    
    
    api = Api(api_name='v1')
    
    api.register(ProductResource())
    
    urlpatterns = [
        path('api/', include(api.urls))
    ]
    ```

    In the `Meta` class of `ProductResource`, you can also precise a class for [authorization](https://django-tastypie.readthedocs.io/en/latest/authorization.html) and [authentication](https://django-tastypie.readthedocs.io/en/latest/authentication.html).

    ```python
    class ProductResource(ModelResource):
        class Meta:
            queryset = Product.objects.all()
            allowed_methods = ['get', "post", "delete", "put"]
            resource_name = 'products'
            fields = ['id', 'user_id', 'name', 'information', 'description', 'price', 'currency', 'date_created']
            authentication = BasicAuthentication()
            validation = FormValidation(form_class=ProductForm)
            authorization = DjangoAuthorization()
    ```

  * Customizable and extendable: The default classes provided by TasyPie are easily extendable. For example, concerning authorizations, you can re-write default permissions methods according to your needs:

        ```python
        from tastypie.authorization import Authorization
        from tastypie.exceptions import Unauthorized
        
        
        class UserObjectsOnlyAuthorization(Authorization):
            def read_list(self, object_list, bundle):
                # This assumes a ``QuerySet`` from ``ModelResource``.
                return object_list.filter(user=bundle.request.user)
        
            def read_detail(self, object_list, bundle):
                # Is the requested object owned by the user?
                return bundle.obj.user == bundle.request.user
        
            def create_list(self, object_list, bundle):
                # Assuming they're auto-assigned to ``user``.
                return object_list
        
            def create_detail(self, object_list, bundle):
                return bundle.obj.user == bundle.request.user
        
            def update_list(self, object_list, bundle):
                allowed = []
        
                # Since they may not all be saved, iterate over them.
                for obj in object_list:
                    if obj.user == bundle.request.user:
                        allowed.append(obj)
        
                return allowed
        
            def update_detail(self, object_list, bundle):
                return bundle.obj.user == bundle.request.user
        
            def delete_list(self, object_list, bundle):
                # Sorry user, no deletes for you!
                raise Unauthorized("Sorry, no deletes.")
        
            def delete_detail(self, object_list, bundle):
                raise Unauthorized("Sorry, no deletes.")
        ```

        You can also write custom authentication classes. In the next example, you can find an example of JWT authentication class in the work.

        ```python
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
        ```

    * Caching, Throttling and validations made easy: If you are a beginner and you are used to forms, you can write the validation logic for a resource using Django forms.

            ```python
            from django import forms
            from tastypie.authorization import Authorization
            from tastypie.resources import ModelResource
            from tastypie.validation import FormValidation
            
            from api.auth.permissions import UserAuthorization
            from api.authentication import JWTAuthentication
            from api.product.models import Product
            
            
            class ProductForm(forms.Form):
                user_id = forms.IntegerField()
                name = forms.CharField(max_length=128)
                information = forms.CharField(max_length=128)
                description = forms.CharField(widget=forms.Textarea)
                price = forms.IntegerField()
                currency = forms.CharField(max_length=10)
            
            
            class ProductResource(ModelResource):
                class Meta:
                    queryset = Product.objects.all()
                    allowed_methods = ['get', "post", "delete", "put"]
                    resource_name = 'products'
                    fields = ['id', 'user_id', 'name', 'information', 'description', 'price', 'currency', 'date_created']
                    authentication = JWTAuthentication()
                    validation = FormValidation(form_class=ProductForm)
                    authorization = UserAuthorization()
            ```

            You can also directly add throttling and caching using a few lines:

      * Caching:

                ```python
                from tastypie.cache import SimpleCache
                    class Meta:
                        queryset = User.objects.all()
                        resource_name = 'auth/user'
                        excludes = ['email', 'password', 'is_superuser']
                        # Add it here.
                        cache = SimpleCache(timeout=10) 
                ```

                In the precedent code, the cache is set for 10 seconds, then updated after 10 seconds have passed.

    * Throttling

            ```python
            from django.contrib.auth.models import User
            from tastypie.resources import ModelResource
            from tastypie.throttle import BaseThrottle
            
            
            class UserResource(ModelResource):
                class Meta:
                    queryset = User.objects.all()
                    resource_name = 'auth/user'
                    excludes = ['email', 'password', 'is_superuser']
                    # Add it here.
                    throttle = BaseThrottle(throttle_at=100)
            ```

            In the precedent code, we will throttle at 100 requests from the same machine.

## Cons

As with any library, TastyPie does not make any exceptions when it comes to having cons. One of the most important cons to identify is the lack of support not similar to the Django REST framework. This means that if you have an error with TastyPie, it will take you time to find someone who had the same issue on the internet.

There is also a lack of resources concerning TastyPie. The documentation is however well written and it should be enough as they tell you how you can extend the features of the library.

Another interesting aspect of Django TastyPie is that it doesn't follow Django principles. For example, in authentication in view classes, you can access the `request.user` object and make some checks with this attribute. In Django TastyPie, you can extend the authentication class to return an object like this, but it will require you to write more code.

Django TastyPie has also a limited set of supported authentication schemes. So if you have a Django authentication package not supporting TasyPie, you will need to write your authentication package. It is worth noting that it doesn't support OAuth either.

Those are the pros and cons of the Django TastyPie library. If you are looking to get started with Django TastyPie, you can find an interesting GitHub repository [here](https://github.com/app-generator/sample-django-tastypie) with User and authentication configured already.

## Conclusion

In this article, we have explored the pros and the cons of the Django TastyPie library. If you are a beginner looking to learn how to build simple API with Django, TastyPie is an interesting tool to explore.
