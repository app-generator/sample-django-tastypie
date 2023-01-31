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

# API Interaction
To interact with api follow the following endpoint:

### list api for product
http://127.0.0.1:8000/api/v1/products/

```
{
    "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
    },
    "objects": [
        {
            "currency": "USD",
            "date_created": "2023-01-29T11:11:38.443682",
            "description": "A simple description goes there",
            "id": 1,
            "information": "IOT",
            "name": "chatGPT home controller",
            "price": 3333,
            "product_sales": [
                {
                    "client": "dfssfd",
                    "currency": "USD",
                    "fee": 44,
                    "id": 1,
                    "payment_type": "cc",
                    "purchase_date": "2023-01-29T11:11:44.574313",
                    "resource_uri": "/api/v1/sales/1/",
                    "state": 44,
                    "value": 444
                }
            ],
            "resource_uri": "/api/v1/products/1/",
            "user_id": 1
        },
        {
            "currency": "USD",
            "date_created": "2023-01-31T08:21:03.990211",
            "description": "A simple description goes there",
            "id": 2,
            "information": "IOT",
            "name": "CybeBOT",
            "price": 10,
            "product_sales": [],
            "resource_uri": "/api/v1/products/2/",
            "user_id": 1
        }
    ]
}
```

### single product api
`http://127.0.0.1:8000/api/v1/products/<product id>/`
 for example: http://127.0.0.1:8000/api/v1/products/1/

Response
 ```
 {
    "currency": "USD",
    "date_created": "2023-01-29T11:11:38.443682",
    "description": "A simple description goes there",
    "id": 1,
    "information": "IOT",
    "name": "chatGPT home controller",
    "price": 3333,
    "product_sales": [
        {
            "client": "dfssfd",
            "currency": "USD",
            "fee": 44,
            "id": 1,
            "payment_type": "cc",
            "purchase_date": "2023-01-29T11:11:44.574313",
            "resource_uri": "/api/v1/sales/1/",
            "state": 44,
            "value": 444
        }
    ],
    "resource_uri": "/api/v1/products/1/",
    "user_id": 1
}
 ```


***You can interact with other api same way***

# Schema
To get all the details API and list of API with it's payload type with `schema`

For example, we want to see product related schema:
http://127.0.0.1:8000/api/v1/products/schema/


```
{
    "allowed_detail_http_methods": [
        "get",
        "post",
        "delete",
        "put"
    ],
    "allowed_list_http_methods": [
        "get",
        "post",
        "delete",
        "put"
    ],
    "default_format": "application/json",
    "default_limit": 20,
    "fields": {
        "currency": {
            "blank": false,
            "default": "USD",
            "help_text": "Unicode string data. Ex: \"Hello World\"",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "string",
            "unique": false,
            "verbose_name": "currency"
        },
        "date_created": {
            "blank": true,
            "default": true,
            "help_text": "A date & time as a string. Ex: \"2010-11-10T03:07:43\"",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "datetime",
            "unique": false,
            "verbose_name": "date created"
        },
        "description": {
            "blank": false,
            "default": "",
            "help_text": "Unicode string data. Ex: \"Hello World\"",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "string",
            "unique": false,
            "verbose_name": "description"
        },
        "id": {
            "blank": true,
            "default": "",
            "help_text": "Integer data. Ex: 2673",
            "nullable": false,
            "primary_key": true,
            "readonly": false,
            "type": "integer",
            "unique": true,
            "verbose_name": "ID"
        },
        "information": {
            "blank": false,
            "default": "No default provided.",
            "help_text": "Unicode string data. Ex: \"Hello World\"",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "string",
            "unique": false,
            "verbose_name": "information"
        },
        "name": {
            "blank": false,
            "default": "No default provided.",
            "help_text": "Unicode string data. Ex: \"Hello World\"",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "string",
            "unique": false,
            "verbose_name": "name"
        },
        "price": {
            "blank": false,
            "default": "No default provided.",
            "help_text": "Integer data. Ex: 2673",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "integer",
            "unique": false,
            "verbose_name": "price"
        },
        "product_sales": {
            "blank": false,
            "default": "No default provided.",
            "help_text": "Many related resources. Can be either a list of URIs or list of individually nested resource data.",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "related_schema": "/api/v1/sales/schema/",
            "related_type": "to_many",
            "type": "related",
            "unique": false,
            "verbose_name": "product sales"
        },
        "resource_uri": {
            "blank": false,
            "default": "No default provided.",
            "help_text": "Unicode string data. Ex: \"Hello World\"",
            "nullable": false,
            "primary_key": false,
            "readonly": true,
            "type": "string",
            "unique": false,
            "verbose_name": "resource uri"
        },
        "user_id": {
            "blank": false,
            "default": 1,
            "help_text": "Integer data. Ex: 2673",
            "nullable": false,
            "primary_key": false,
            "readonly": false,
            "type": "integer",
            "unique": false,
            "verbose_name": "user id"
        }
    }
}
```