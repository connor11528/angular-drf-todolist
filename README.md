angular-drf-todolist
====

In this app we'll build a persistent todo list. The backend and database will be handled by django. django rest framework will convert the tabled data to JSON and angular will bring the frontend magic.

![this is angular](http://cloud-4.steamusercontent.com/ugc/541889413256781007/8E0E1D04169BD1922CA1467046699255CEB69E02/)

### Clone the starter project

I made a [angular-drf starter project](git@github.com:jasonshark/django-drf-angular-starter-project.git). We're going to start from there and build out the todolist. Clone it and give it a new name

```
$ git clone git@github.com:jasonshark/django-drf-angular-starter-project.git
$ mv django-drf-angular-starter-project angular-drf-todolist
$ cd angular-drf-todolist
```

### Set up virtual environment

We do this so we install the packages locally instead of to your machine. Our project dependencies are specified in `requirements.txt`.

```
$ source ~/.bash_profile
$ mkvirtualenv angular-drf-todolist
$ lsvirtualenv
$ pip install -r requirements.txt
```

### Launch server

```
$ ./manage.py migrate
$ ./manage.py runserver
```

This sets up our database and starts the server. Go to `localhost:8000`. Now angular and drf play nicely

![django on the right](http://i62.tinypic.com/2z3uvfb.png)

### Create Todo model

This is the same as creating a table in our database to hold all of the todos. Each todo will take up a row in the table. The model defines what the columns are going to be. For each todo we'll have a title, description and is_completed.

**jsframework/models.py**
```
from django.db import models

class Todo(models.Model):
    title = models.CharField(max_length=75)
    description = models.TextField()
    is_completed = models.BooleanField()

    def __unicode__(self):
        return self.title
```

Then make the migrations that turns the above python into a database table: 

```
$ ./manage.py makemigrations
$ ./manage.py migrate
```

Check that it worked by opening up the shell and adding a todo:

```
$ ./manage.py shell
>>> from jsframework.models import Todo
>>> Todo.objects.all()
[]
>>> first_todo = Todo(title='first todo',description='a little bit softer now',is_completed='false')
>>> first_todo.save()
[<Todo: first todo>]
```

At first there's nothing, now it looks like we added a todo to the database. Really we want to display this in the browser as JSON so angular can play with it.

### Serialize to JSON

Create a TodoSerializer in a new file `jsframework/serializers.py`. This will convert our data into json.

```
from rest_framework import serializers
from jsframework.models import Todo

class TodoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Todo
```

Now prep our views for rendering JSON:

```
from rest_framework import viewsets

from jsframework.models import Todo
from serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer
```

And then define the routes in `jsframework/urls.py`. These will define where and what JSON should be displayed.

```
from django.conf.urls import patterns, include, url
from rest_framework import routers
from . import views

todo_router = routers.DefaultRouter()
todo_router.register(r'todos', views.TodoViewSet, base_name='todos')

urlpatterns = [
	# Send base.html to angular
    url(r'^$', views.index, name='index'),

    url('^api/todos', include(todo_router.urls)),
]
```


Hit `http://localhost:8000/api/todos` in your browser and you'll see output.
