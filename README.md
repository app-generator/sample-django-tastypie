# [Django Tastypie](https://github.com/app-generator/sample-django-tastypie) `Sample`

Playground project built on top of [django-tastypie](https://github.com/django-tastypie/django-tastypie) that aims to translate automatically OpenAPI definitions into secure APIs without coding.

<br />

> Product Roadmap 

| Status | Item | info | 
| --- | --- | --- |
| **Phase 1#** |  |  |
| ✅ | `Up-to-date Dependencies` |  |
| ✅ | [django-tastypie](https://github.com/django-tastypie/django-tastypie) Integration |  |
| ✅ | **Persistence** | `SQLite`, `MySql` |
| ✅ | **Basic Authentication** | classic user/password |
| ✅ | **API** | Products & Sales (linked tables) |
|     |         | GET Requests (public), `get/`, `get/id`  |
|     |         | CREATE, UPD, DEL - reserved for authenticated users |
| **Phase 2#** |  |  |
| ✅ | `OpenAPI Parser` integration |  |
| ✅ | `Complete the flow` | OpenAPI -> APIs |

<br />

## ✨ Start the app in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`) 

```bash
$ git clone https://github.com/app-generator/sample-django-tastypie.git
$ cd sample-django-tastypie
```

<br />

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build 
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

## Manual Build 

> 👉 Download the code  

```bash
$ git clone https://github.com/app-generator/sample-django-tastypie.git
$ cd sample-django-tastypie
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

> 👉 How to use

This project provides endpoints for authentication, user profiles, products, and sales. The users, products, and sales endpoints require the developer to pass a JWT token in the headers with the following format `Authorization: Bearer <JWT Token>` that you can obtain by login at the `/api/v1/auth/login/` endpoint. 

```json
POST /api/v1/auth/login/
{
	"password": "12345678",
	"username": "koladev33@gmail.com"
}
```

> Note: To register, you can send a POST request to this endpoint `/api/v1/auth/` with a `password`, `username`, and `email` fields present in the payload. 

The request on the `login` endpoint will return a JWT token you can grab to make requests on the `/api/v1/products/`, `/api/v1/users/` and `/api/v1/sales/`. 

**Validation**

Tastypie allows you to write validation schemes using Django forms. You can find an example of this at `api/sale/api.py`.

```python
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
        ...
        validation = FormValidation(form_class=SaleForm)
        authorization = UserAuthorization()

```

---
[Django Tastypie](https://github.com/app-generator/sample-django-tastypie) `Sample` - Open-source Starter provided by **[AppSeed](https://appseed.us/)**
