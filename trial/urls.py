from django.conf.urls import patterns, url
from trial.views import (PostDetialView)

urlpatterns = patterns(
    '',
    url(
        r'(?P<pk>[0-9]+)/$',
        PostDetialView.as_view(),
        name='post'),
)
