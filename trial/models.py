from django.db import models
from django.contrib.contenttypes.fields import (
    GenericRelation)
from comments.models import Comment


class Post(models.Model):
    post = models.CharField(max_length=200)
    comments = GenericRelation(Comment)
