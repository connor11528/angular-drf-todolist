django-drf-angular-starter-project
====

Create an app with django rest framework (drf) that uses angular.js on the frontend. This app will be built from the [django-drf-starter-project](https://github.com/jasonshark/django-drf-starter-project). If you are curious about how the django-drf-starter-project was built you can view the [tutorial here](https://coderwall.com/p/ympo6g/create-a-starter-template-for-working-with-django-rest-framework?p=1&q=).

![Let's get started](http://media.giphy.com/media/mxDZecDOOsWCA/giphy.gif)


### Create the project
```
$ git clone git@github.com:jasonshark/django-drf-starter-project.git
$ mv django-drf-starter-project django-drf-angular-starter-project
$ cd django-drf-angular-starter-project
```

This downloads the code from part one and renames the project to angular name.

### Set up virtual environment

```
$ source ~/.bash_profile
$ mkvirtualenv django-drf-angular-starter-project # OR $ workon django-drf-angular-starter-project if you've already created the virtual environment
$ lsvirtualenv
$ pip install -r requirements.txt
```

On my computer I have to source .bash_profile. I'm lazy and haven't fixed this. Hopefully you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) set up properly on your own machine. The last step installs django and django rest framework from requirements.txt.


### Modify view

In the views last time we used django templates, now we want angular to handle the front end. Django will provide one template (`jsframework/templates/jsframework/base.html`). The rest of our frontend code will be stored in `jsframework/static/templates`. Angular will access this using [ui-router](https://github.com/angular-ui/ui-router).

Send the base template 

**jsframework/views.py:**
```
from django.shortcuts import render

def index(request):
    return render(request, 'jsframework/base.html')
```

Then in base.html modify it to load angular and use angular views. Delete the django template tags, add:

```
<html ng-app='drf-angular'>

...

<div ui-view></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.15/angular.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/angular-ui-router/0.2.15/angular-ui-router.js"></script>
```

### Write angular
![don't get carried away](http://cdn.meme.am/instances/500x/62550074.jpg)

Create an app, routes and a controller:

```
var app = angular.module('drf-angular', [
    'ui.router'
]);

app.config(function($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('home', {
            url: '/',
            templateUrl: '/static/templates/home.html',
            controller: 'MainCtrl'
        });

    $urlRouterProvider.otherwise('/');
});

app.controller('MainCtrl', function($scope){
    $scope.test = "I come from the angularz";
});
```

All of our angular templates will live in `jsframework/static/templates`. Reference them using the path specified in `templateUrl`.

All our routing will have `/#/`. Also we have not invented any models or serializers, but we've set up a server and handling angular on the frontend.