from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)

    comment = models.CharField(max_length=512)
    likes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])
