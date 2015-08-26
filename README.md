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

###Step 1
In your models.py add the field comments to the model for which comments should be added (e.g. Blog) and the appropriate imports as shown below

```python
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment

class Blog(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=256)
	body = models.TextField()
	comments = GenericRelation(Comment)
```

###Step 2
In your template (e.g. blog-detail.html) add the following template tags where object is the instance of blog.

```html
{% load comments_tags %}
{% get_comments object request.user %}
```

This requires jQuery. Make sure to add the following to your template if you're not already loading jQuery locally
```html
<script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
<script src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
```
