#`django-ajax-comments` Comments

`django-ajax-comments` is an application for Django-powered websites.

It allows you to integrate commenting functionality to any model you have eg. blogs, pictures, etc...

List of actions you can do:
* Add a comment
* Edit a comment you posted (Authenticated)
* Delete a comment you posted (Authenticated)
* Like a comment (Authenticated)

##Installation

Installation is available via `pip`

`$ pip install django-ajax-comments`

or through source on github

```
$ git clone https://github.com/dreidev/Comments.git
$ cd Comments
$ python setup.py install
```

You now need to add `django-ajax-comments` to your `INSTALLED_APPS` in `settings.py` and modify `urls.py` which are both in your your project's directory.

In your `settings.py` file it should go like, note that you should add it somewhere after `django.contrib.auth`:

```python
INSTALLED_APPS = (
	'django.contrib.auth',
	...
	'comments',
	..
)
```
