from django.test import TestCase, Client
from .models import Comment, Like
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AddCommentTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='johndoe', password='123456')
        self.client.login(username='johndoe', password='123456')

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

    def test_delete_comment_comment_not_existing(self):
        init_comment_count = Comment.objects.all().count()
        response = self.client.get(
            reverse('comment-delete', kwargs={'pk': 1}),
            {},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), init_comment_count)


class LikeCommentTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='johndoe', password='123456')
        self.client.login(username='johndoe', password='123456')

    def test_like_comment(self):
        """
        Tests that an authenticated user can like a comment.
        """
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_likes_count = Like.objects.all().count()
        response = self.client.get(
            reverse('comment-like'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count+1)

    def test_unlike_comment(self):
        """
        Tests that an authenticated user can unlike a comment he liked
        """
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_likes_count = Like.objects.all().count()
        response = self.client.get(
            reverse('comment-like'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count+1)
        response = self.client.get(
            reverse('comment-unlike'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count)

    def test_like_comment_not_authenticated(self):
        """
        Tests that a guest (not authenticated) cannot like a comment
        """
        self.client.logout()
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_likes_count = Like.objects.all().count()
        response = self.client.get(
            reverse('comment-like'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count)

    def test_unlike_comment_not_authenticated(self):
        """
        Tests that a guest (not authenticated) cannot unlike a comment
        """
        self.client.logout()
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_likes_count = Like.objects.all().count()
        response = self.client.get(
            reverse('comment-unlike'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count)

    def test_unlike_comment_without_like(self):
        """
        Tests that an authenticated user cannot
        unlike a comment they didn't like
        """
        self.client.post(
            reverse('comment-create'),
            {'comment': 'form'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        init_likes_count = Like.objects.all().count()
        response = self.client.get(
            reverse('comment-unlike'),
            {'comment_id': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Like.objects.all().count(), init_likes_count)


class EditCommentTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(username='johndoe', password='123456')
        self.client.login(username='johndoe', password='123456')

    def test_edit_comment_owner(self):
        user = User.objects.create_user(username='john',
                                        password='glass onion')
        self.client.login(username='john', password='glass onion')
        comment = Comment.objects.create(
            user_id=user.id, comment="trial comment")
        response = self.client.post(
            reverse('comment-update', kwargs={'pk': comment.id}),
            {'user': user.id, 'comment': 'trial'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.get(id=comment.id).comment, 'trial')

    def test_edit_not_authentiated(self):
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
            Comment.objects.get(id=comment.id).comment, 'trial comment')
        self.assertEqual(response.content, 'not authenticated')

    def test_edit_no_owner(self):
        comment = Comment.objects.create(comment="trial comment")
        response = self.client.post(
            reverse('comment-update', kwargs={'pk': comment.id}),
            {'comment': 'trial'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Comment.objects.get(id=comment.id).comment, 'trial comment')
        self.assertEqual(response.content, 'not allowed')
