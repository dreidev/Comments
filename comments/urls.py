from django.conf.urls import patterns, url
from .views import (
    CommentListView, CommentCreateView, CommentDeleteView,
    LikeComment, UnlikeComment)

urlpatterns = patterns(
    '',
    url(r'^$', CommentListView.as_view(), name='comment-list'),
    url(r'^create/$', CommentCreateView.as_view(), name='comment-create'),
    url(r'^delete/(?P<pk>[-\w]+)$',
        CommentDeleteView.as_view(), name='comment-delete'),
    url(r'^like/$', LikeComment.as_view(), name='comment-like'),
    url(r'^unlike/$', UnlikeComment.as_view(), name='comment-unlike'),
)
