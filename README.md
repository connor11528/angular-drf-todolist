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

# Launch server

```
$ ./manage.py migrate
$ ./manage.py runserver
```

This sets up our database and starts the server. Go to `localhost:8000`. Now angular and drf play nicely

![django on the right](http://i62.tinypic.com/2z3uvfb.png)
