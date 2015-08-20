from django.conf.urls import patterns, url
from .views import (CommentListView, CommentCreateView,
                    CommentDeleteView, CommentUpdateView
                    )

urlpatterns = patterns(
    '',
    url(r'^$', CommentListView.as_view(), name='comment-list'),
    url(r'^create/$', CommentCreateView.as_view(), name='comment-create'),
    url(
        r'update/(?P<pk>[0-9]+)/$',
        CommentUpdateView.as_view(),
        name='comment-update'),
    url(r'^delete/(?P<pk>[-\w]+)$',
        CommentDeleteView.as_view(), name='comment-delete'),
)
