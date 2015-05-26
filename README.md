django_drf_starter_project
====

### Set up virtual environment

```
$ source ~/.bash_profile
$ lsvirtualenv
$ mkvirtualenv django-drf-starter-project # OR $ workon django-drf-starter-project
```

### Create django app

```
$ django-admin startproject django_drf_starter_project
$ cd django_drf_starter_project
$ pip install django djangorestframework
$ pip freeze > requirements.txt
$ ./manage.py runserver
```

You should see "It worked!" at localhost:8000. (control + C stops server on mac). If you're using git also copy and paste in the `.gitignore` file from here so you don't commit garbage to version control.

### Create a new app

```
$ ./manage.py startapp jsframework
$ mkdir jsframework/templates
$ mkdir jsframework/templates/jsframework
$ touch jsframework/templates/jsframework/index.html jsframework/templates/jsframework/base.html
```

This creates a new app called jsframework within the django_drf_starter_project project. We also set up a templates folder where we will display our html templates. I made another folder called jsframework inside the templates directory. I know it looks a bit weird. We do this so we can namespace our templates later on when declaring routes. Django will automagically look in the `templates` directory for every app when compiling templates.

### Let django know about it

Modify `django_drf_starter_project/settings.py` to include the rest_framework app that we installed via pip and our jsframework app we created from the cli.

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'jsframework',
)
```

Also sync your database. Django will use sqlite as default. Run `./manage.py migrate` after updating your installed apps. A `db.sqlite3` file will get generated automagically. Our database is now in sync.

![migrate it](http://media.giphy.com/media/XdlEHQpoHhy0g/giphy.gif)

### Render templates to browser

