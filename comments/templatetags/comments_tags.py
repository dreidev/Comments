from django import template
from comments.models import Like
from comments.forms import CommentForm
from django.conf import settings


register = template.Library()


@register.simple_tag(name='get_model_name')
def get_model_name(object):
    """ returns the model name of an object """
    return type(object).__name__


@register.simple_tag(name='get_app_name')
def get_app_name(object):
    """ returns the app name of an object """
    return type(object)._meta.app_label


@register.simple_tag(name='get_comment_count')
def get_comment_count(object):
    """ returns the count of comments of an object """
    print object
    model_object = type(object).objects.get(id=object.id)
    return model_object.comments.all().count()


def get_comments(object, user):
    """
    Retrieves list of comments related to a certain object and renders
    The appropriate template to view it
    """
    model_object = type(object).objects.get(id=object.id)
    comments = model_object.comments.all()
    liked = []
    for comment in comments:
        try:
            Like.objects.get(user=user, comment=comment)
            liked.append(True)
        except:
            liked.append(False)
    return {"form": CommentForm(),
            "comment_liked": zip(comments, liked),
            "target": object,
            "user": user,
            "comments_count": comments.count(),
            "allow_likes": getattr(
                settings,
                'COMMENTS_ALLOW_LIKES',
                True)}

register.inclusion_tag('comments/comments.html')(get_comments)


def comment_form(object, user):
    """
    renders template of comment form
    """
    return {"form": CommentForm(),
            "target": object,
            "user": user,
            "allow_anonymous": getattr(
                settings,
                'COMMENTS_ALLOW_ANONYMOUS',
                False)}


register.inclusion_tag('comments/comment_form.html')(comment_form)


def include_jQuery():
    return

register.inclusion_tag('comments/jQuery.html')(include_jQuery)
