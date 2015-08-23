from django.test import TestCase
from .models import Comment
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


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

    def test_add_comment(self):
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


class EditCommentTestCase(TestCase):

    def test_edit_comment_owner(self):
        user = User.objects.create_user(username='john',
                                        password='glass onion')
        comment = Comment.objects.create(
            user_id=user.id, comment="trial comment")
        response = self.client.post(
            reverse('comment-update', kwargs={'pk': comment.id}),
            {'user': user.id, 'comment': 'trial'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.get(id=comment.id).comment, 'trial')
