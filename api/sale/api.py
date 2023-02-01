from django import forms
from django.core.exceptions import ValidationError
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from api.auth.permissions import UserAuthorization
from api.authentication import JWTAuthentication
from api.product.models import Product
from api.sale.models import Sale
from tastypie.serializers import Serializer


class SaleForm(forms.Form):
    product = forms.IntegerField()
    state = forms.IntegerField()
    value = forms.IntegerField()
    fee = forms.IntegerField()
    client = forms.CharField(max_length=128)
    currency = forms.CharField(max_length=10, required=False)
    payment_type = forms.CharField(max_length=10, required=False)

    def clean_product(self):
        product_id = self.cleaned_data['product']

        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            raise ValidationError("This product doesn't exist.")


class SaleResource(ModelResource):
    class Meta:
        queryset = Sale.objects.all()
        allowed_methods = ['get', "post", "delete", "put"]
        resource_name = 'sales'
        fields = ['id', 'product', 'state', 'value', 'fee', 'client', 'currency', 'payment_type', 'purchase_date']
        authentication = JWTAuthentication()
        validation = FormValidation(form_class=SaleForm)
        authorization = UserAuthorization()

    def to_yaml(self,bundle, options):
        return Serializer.from_yaml(self, bundle)


