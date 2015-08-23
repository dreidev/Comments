from django.test import TestCase
from .models import Comment
from django.core.urlresolvers import reverse


class AddCommentTestCase(TestCase):

    def test_add_comment(self):
        init_comment_count = Comment.objects.all().count()
        response = self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), init_comment_count + 1)

    def test_comment_must_exist(self):
        init_comment_count = Comment.objects.all().count()
        self.client.post(
            reverse('comment-create'),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(Comment.objects.all().count(), init_comment_count)


class DeleteCommentTestCase(TestCase):

    def test_delete_comment(self):
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_comment_count = Comment.objects.all().count()
        response = self.client.get(
            reverse('comment-delete', kwargs={'pk': 1}),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), init_comment_count)
