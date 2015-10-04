#`django-ajax-comments` Comments

<!-- [![alt text][logo]](https://readthedocs.org/projects/comments/builds/)

[logo]: https://readthedocs.org/projects/pip/badge/?version=latest "Build Passing" -->

[![Coverage Status](https://coveralls.io/repos/dreidev/Comments/badge.svg?branch=HEAD&service=github)](https://coveralls.io/github/dreidev/Comments?branch=HEAD)

[![Build Status](https://travis-ci.org/dreidev/Comments.svg?branch=master)](https://travis-ci.org/dreidev/Comments)

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
    url(r'^comments/', include('comments.urls')),
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

```python
{% load comments_tags %}  # Loading the template tag
{% get_comments object request.user %}  # Include all the comments belonging to a certain object
{% comment_form object request.user %}  # Include the form for adding comments
{% get_comment_count object %}  # Include the number of comments on a certain object
```
The last template tag `{% get_comment_count object %}` is already included in `{% get_comments %}`, however you could include it seperately anywhere you want.

---

This requires jQuery. If you're not already including it, we have a template tag that you can include in your html.
######It should be added after `{% load comments_tags %}` directly.
```python
{% load comments_tags %}
{% include_jQuery %}
```

##Settings
In `settings.py` you could set some settings for the application

####`COMMENTS_ALLOW_ANONYMOUS`
>Its default is `False`.                                                                                                                   
>If set to `True`, anonymous users will be allowed to post comments.

To set it to `True`, add the following to `settings.py`:
```python
COMMENTS_ALLOW_ANONYMOUS = True
```

####`COMMENTS_ALLOW_LIKES`
>Its default is `True`.                                                                                                                   
>It allows authenticated users to like/unlike comments.

To change the default, add the following to `settings.py`:
```python
COMMENTS_ALLOW_LIKES = False
```

##Styling
If you want to customize the way your comments look follow the following steps:
* In your template directory, create a folder and call it comments
* Retrieve the html templates for the comments application from its directory which can be found in your sitepackages and github as well.
* Manipulate those templates as you see fit by adding css classes and such.

and you're done.
