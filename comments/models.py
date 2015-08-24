from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)

    comment = models.CharField(max_length=512)
    likes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')


class Like(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
