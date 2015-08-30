from django.conf.urls import patterns, url
from .views import (
    CommentCreateView, CommentDeleteView,
    LikeComment, UnlikeComment, CommentUpdateView)

urlpatterns = patterns(
    '',
    url(r'^create/$', CommentCreateView.as_view(), name='comment-create'),
    url(
        r'update/(?P<pk>[0-9]+)/$',
        CommentUpdateView.as_view(),
        name='comment-update'),
    url(r'^delete/(?P<pk>[-\w]+)$',
        CommentDeleteView.as_view(), name='comment-delete'),
    url(r'^like/$', LikeComment.as_view(), name='comment-like'),
    url(r'^unlike/$', UnlikeComment.as_view(), name='comment-unlike'),
)
