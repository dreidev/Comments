from django import template
from comments.models import Like
from comments.forms import CommentForm

register = template.Library()


@register.simple_tag(name='get_model_name')
def get_model_name(object):
    """ returns the model name of an object """
    return type(object).__name__


@register.simple_tag(name='get_app_name')
def get_app_name(object):
    """ returns the app name of an object """
    return type(object)._meta.app_label


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
            "user": user}

register.inclusion_tag('comments/comments.html')(get_comments)
