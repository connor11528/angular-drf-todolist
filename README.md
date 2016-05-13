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
    is_completed = models.BooleanField(default=False)

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
from django.shortcuts import render
from rest_framework import viewsets

from jsframework.models import Todo
from serializers import TodoSerializer

# Todos routes automatically generated
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


# Home route to send template to angular
def index(request):
    return render(request, 'jsframework/base.html')
```

We use the [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) which automatically provides us endpoints for `.list()`, `.retrieve()`, `.create()`, `.update()`, and `.destroy()`. This is where DRF magic really happens. With that small class above we have the views necessary to create, read, update and delete todos. In the router we're going to map these out.

Update our routes in `jsframework/urls.py`. These will define where and what JSON should be displayed.

```
from django.conf.urls import patterns, include, url
from rest_framework import routers
from . import views

todo_router = routers.DefaultRouter()
todo_router.register(r'todos', views.TodoViewSet, base_name='todos')

urlpatterns = [
    # Send base.html to angular
    url(r'^$', views.index, name='index'),

    url('^api/', include(todo_router.urls)),
]
```

Hit `http://localhost:8000/api/todos` in your browser and you'll see a JSON array of Todo objects in the nice DRF console. There are buttons for creating (using PUT requests), updating (PUT requests) and deleting (DELETE requests).


### Hook this sucker up to the frontend

We are going to go a bit quick over the angular stuff because there's a full functional API.

First define the routes and a constant for our API endpoint.

```
var app = angular.module('drf-angular', [
    'ui.router'
]);

app.constant('BASE_URL', 'http://localhost:8000/api/todos/');

app.config(function($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: '/static/templates/home.html',
            controller: 'MainCtrl'
        })
        .state('add-todo', {
            url: "/add",
            templateUrl: 'static/templates/add_todo.html',
            controller: 'MainCtrl'
        });

    $urlRouterProvider.otherwise('/');
});
```

Special note, we are using [ui-router](https://github.com/angular-ui/ui-router). Also, make sure you have trailing slashes on your urls when making requests to DRF. The trailing slash had us stumped for a bit.

```
// will break without slash at the end
app.constant('BASE_URL', 'http://localhost:8000/api/todos/');
```

Then define a service that makes requests to DRF and returns promises. We probably could have used [$resource](https://docs.angularjs.org/api/ngResource/service/$resource) or [Restangular](https://github.com/mgonto/restangular) here but I am not very familiar with them and do not know if they will survive in Angular 2.0. $http is simple and straight forward. Make http requests and return promises.

```
app.service('Todos', function($http, BASE_URL){
    var Todos = {};

    Todos.all = function(){
        return $http.get(BASE_URL);
    };

    Todos.update = function(updatedTodo){
        return $http.put(BASE_URL + updatedTodo.id, updatedTodo);
    };

    Todos.delete = function(id){
        return $http.delete(BASE_URL + id + '/');
    };

    Todos.addOne = function(newTodo){
        return $http.post(BASE_URL, newTodo)
    };

    return Todos;
});
```

Call the service methods in the controller:

```
app.controller('MainCtrl', function($scope, Todos, $state){
    $scope.newTodo = {};
    $scope.addTodo = function() {
        Todos.addOne($scope.newTodo)
            .then(function(res){
                // redirect to homepage once added
                $state.go('home');
            });
    };

    $scope.toggleCompleted = function(todo) {
        Todos.update(todo);
    };

    $scope.deleteTodo = function(id){
        Todos.delete(id);
        // update the list in ui
        $scope.todos = $scope.todos.filter(function(todo){
            return todo.id !== id;
        })
    };

    Todos.all().then(function(res){
        $scope.todos = res.data;
    });
});
```

The delete function is a bit tricky. We have to update `$scope.todos` on the client and we don't really want to run the digest cycle again or send another http request, there's no need. We could do some error handling to make sure the todo was *really* deleted from the database. Here we filter the normal array, if the id property matches the one we want to delete get rid of it. This solution came from [StacktotheOverflow](http://stackoverflow.com/questions/10024866/remove-object-from-array-using-javascript).

### Add add the markup

**jsframework/static/templates/home.html**
```
<div class='row text-center'>
    <div class='col-sm-4 col-sm-offset-4'>
        <h1>All Todos</h1>

        <button ui-sref="add-todo" class='btn btn-primary btn-lg' style='margin-bottom:20px;'>Add Todo</button>

        <ul class="list-group">
            <li ng-repeat='todo in todos' ng-class="{completed: todo.is_completed}" class="list-group-item">
                <input type="checkbox" ng-checked="todo.is_completed" ng-change="toggleCompleted(todo)" ng-model='todo.is_completed'>  {{todo.title}}

                <span class='badge' ng-click="deleteTodo(todo.id)">X</span>
            </li>
        </ul>
    </div>
</div>
```

The markup will `ng-repeat` over the todos. [ng-change](https://docs.angularjs.org/api/ng/directive/ngChange) is a nifty directive that executes a function when whatever you pass to it is updated or changed. I stole this from the [Angular.js TodoMVC](https://github.com/tastejs/todomvc/tree/gh-pages/examples/angularjs) implementation. [ng-checked](https://docs.angularjs.org/api/ng/directive/ngChecked) will check the checkbox based on the truthy or falsey value we pass to it. [ng-class](https://docs.angularjs.org/api/ng/directive/ngClass) is also kind of cool. [scotch.io](https://scotch.io/tutorials/the-many-ways-to-use-ngclass) has a tutorial there about the many ways to use ngClass.

The CSS for this project is mad simple:

```
.completed {
    text-decoration: line-through;
}

.badge {
    cursor: pointer;
}
```

Then we have a page to add a todo:

**jsframework/static/templates/add_todo.html**

```
<div class='row text-center'>
    <div class='col-sm-4 col-sm-offset-4'>
        <h1>Add a todo</h1>
        <input type="text" ng-model="newTodo.title" placeholder="title" class='form-control' />
        <textarea name="textarea" class="form-control" rows="5" ng-model="newTodo.description" placeholder="description"></textarea>
        <button class='btn btn-success btn-lg' ng-click="addTodo()">Add</button>
    </div>
</div>
```

![](http://media3.giphy.com/media/jYAGkoghdmD9S/giphy.gif)

If you like the tutorial give the [repo](https://github.com/connor11528/angular-drf-todolist) a star!
