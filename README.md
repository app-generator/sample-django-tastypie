# Django Tastypie `Sample`

Playground project built on top of [django-tastypie](https://github.com/django-tastypie/django-tastypie) that aims to translate automatically OpenAPI definitions into secure APIs without coding.

<br />

> Product Roadmap 

| Status | Item | info | 
| --- | --- | --- |
| Phase 1# | - | - |
| ❌ | `Up-to-date Dependencies` | - |
| ❌ | [django-tastypie](https://github.com/django-tastypie/django-tastypie) Integration | - |
| ❌ | **Persistence** | `SQLite`, `MySql` |
| ❌ | **Basic Authentication** | classic user/password |
| ❌ | **API** | Products & Sales (linked tables) |
|     |         | GET Requests (public), `get/`, `get/id`  |
|     |         | Mutating requests (Create, UPD, DEL) (reserved for authenticated users) |
| - | - | - |
| Phase 2# | - | - |
| ❌ | `OpenAPI Parser` integration | - |
| ❌ | Complet the flow | OpenAPI -> APIs |

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

---
Django Tastypie `Sample` - Open-source Starter provided by **[AppSeed](https://appseed.us/)**
