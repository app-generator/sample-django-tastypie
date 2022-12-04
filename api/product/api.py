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



