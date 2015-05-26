django-drf-angular-starter-project
====

Create an app with django rest framework (drf) that uses angular.js on the frontend. This app will be built from the [django-drf-starter-project](https://github.com/jasonshark/django-drf-starter-project). If you are curious about how the django-drf-starter-project was built you can view the [tutorial here](https://coderwall.com/p/ympo6g/create-a-starter-template-for-working-with-django-rest-framework?p=1&q=).

### Create the project
```
$ git clone git@github.com:jasonshark/django-drf-starter-project.git
$ mv django-drf-starter-project django-drf-angular-starter-project
$ cd django-drf-angular-starter-project
```

This downloads the [code](https://github.com/jasonshark/django-drf-starter-project) from part one and renames the project to angular name.

### Set up virtual environment

```
$ source ~/.bash_profile
$ mkvirtualenv django-drf-angular-starter-project # OR $ workon django-drf-angular-starter-project if you've already created the virtual environment
$ lsvirtualenv
$ pip install -r requirements.txt
```

On my computer I have to source .bash_profile. I'm lazy and haven't fixed this. Hopefully you have [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) set up properly on your own machine. The last step installs django and django rest framework.

### Tie it together with git

So there's the base repo that has drf setup, then there's this one for specifically angular-drf integration. Essentially this repo inherits from jasonshark/django-drf-starter-project. If I change that repo I want to pull in those changes in to this repo. Here's how we do that:

```
$ git remote rename origin upstream
$ git remote add origin <github_url>
$ git remote -v
origin  git@github.com:jasonshark/django-drf-angular-starter-project.git (fetch)
origin  git@github.com:jasonshark/django-drf-angular-starter-project.git (push)
upstream    git@github.com:jasonshark/django-drf-starter-project.git (fetch)
upstream    git@github.com:jasonshark/django-drf-starter-project.git (push)
```

So now I can push to this repo for the angular integration code and use `git pull upstream master` to take in changes from jasonshark/django-drf-starter-project.

