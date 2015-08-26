#`django-ajax-comments` Comments

`django-ajax-comments` is a commenting application for Django-powered websites.

It allows you to integrate commenting functionality to any model you have eg. blogs, pictures, etc...

List of actions you can do:
* Add a comment
* Edit a comment you posted (Authenticated)
* Delete a comment you posted (Authenticated)
* Like a comment (Authenticated)

####All actions are done through ajax

##Installation

Installation is available via `pip`

`$ pip install django-ajax-comments`

or via source on github

```
$ git clone https://github.com/dreidev/Comments.git
$ cd Comments
$ python setup.py install
```

Add 'comments' to your installed_apps in your `settings.py` file. It should look like the following. Note that you should add it after `django.contrib.auth`:

```python
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	...
	'comments',
	..
)
```

In your urls.py:

```python
urlpatterns = patterns('',
    ...
    url('^comments/', include('comments.urls')),
    ...
)
```


##Migrations for Django 1.7 and later

Migrate comments:
```
$ python manage.py migrate comments
```


##Setup

