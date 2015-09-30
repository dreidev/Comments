from django.views.generic import (
    CreateView, DeleteView, FormView,
    UpdateView)
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.middleware.csrf import get_token
from comments.models import Comment, Like
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class AjaxableResponseMixin(object):

    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse({
                'success': 0,
                'error': form.errors})
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            csrf_token_value = get_token(self.request)
            html = render_to_string(
                "comments/comment.html",
                {'object': self.object,
                 'user': self.request.user,
                 'form': CommentForm(),
                 'liked': False,
                 'csrf_token': csrf_token_value,
                 'allow_likes': getattr(
                    settings,
                    'COMMENTS_ALLOW_LIKES',
                    True)
                 })
            try:
                data = {
                    'success': 1,
                    'html': html,
                    'id': self.object.id
                }
            except:
                data = {
                    'success': 1,
                }
            return JsonResponse(data)
        else:
            return response


class CommentCreateView(AjaxableResponseMixin, CreateView):

    """
    Class that creates an instance of model:comment.Comment

    """
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_form.html'
    success_url = reverse_lazy('comment-create')

    def form_valid(self, form):
        comment = form.save(commit=False)
        try:
            content_type = ContentType.objects.get(
                app_label=self.request.POST['app_name'],
                model=self.request.POST['model'].lower())
            model_object = content_type.get_object_for_this_type(
                id=self.request.POST['model_id'])
            comment.content_object = model_object
        except:
            pass
        comment.save()
        return super(CommentCreateView, self).form_valid(form)


class CommentDeleteView(DeleteView):

    """
    Class that deletes an instance of model:comment.Comment

    """
    model = Comment
    success_url = reverse_lazy('comment-create')

    def get(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        try:
            id = request.GET['id']
            self.object = Comment.objects.get(id=id)
            if (self.object.user.id == request.user.id):
                self.object.delete()
                data = {"success": "1",
                        "count": Comment.objects.count()}
            else:
                data = {"success": "0"}
        except:
            data = {"success": "0"}
        if request.is_ajax():
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(self.success_url)


class LikeComment(FormView):

    """
    Class that creates an instance of model:comment.Like
    """

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        likes_count = 0
        data = {}

        # Check if user is authenticated.
        if not request.user.is_authenticated():
            # Return if user is not authenticated.
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)

        user = request.user
        try:
            # Check if the comment with the requested id exists.
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                # Check if the user already liked the comment,
                # Do nothing in this case.
                Like.objects.get(comment=comment, user=user)
                data['success'] = 0
                data['error'] = "You have already liked this comment"
            except:
                # Create a like on the comment in case the user hasn't
                # liked it already.
                Like.objects.create(comment=comment, user=user).save()
                likes_count += 1
                comment.likes_count = likes_count
                comment.save()
                data['likes_count'] = likes_count
                data['success'] = 1
        except:
            # Return an error where the comment might have been removed.
            data['success'] = 0
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)


class UnlikeComment(FormView):

    """
    Class that deletes an instance of model:comment.Like
    """

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        likes_count = 0
        data = {}

        # Check if user is authenticated.
        if not request.user.is_authenticated():
            # Return if user is not authenticated.
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)

        user = request.user
        try:
            # Check if the comment with the requested id exists.
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                # Check if the user already liked the comment,
                # Unlike the comment in this case.
                Like.objects.get(comment=comment, user=user).delete()
                likes_count -= 1
                comment.likes_count = likes_count
                comment.save()
                data['success'] = 1
                data['likes_count'] = likes_count
            except:
                # If the user hasn't liked it, return an error.
                data['success'] = 0
                data['error'] = "You have to like the comment first"
        except:
            # Return an error where the comment might have been removed.
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)


class CommentUpdateView(AjaxableResponseMixin, UpdateView):

    """
    Class that updates an instance of model:comment.Comment
    """
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_edit_form.html'
    success_url = reverse_lazy('comment-create')

    def form_valid(self, form):
        if not self.object.user:
            return HttpResponse('not allowed')
        else:
            if (self.request.user.is_authenticated and
                    self.object.user == self.request.user):
                form.save()
                return super(CommentUpdateView, self).form_valid(form)
            else:
                return HttpResponse('not authenticated')

    def is_valid(self, form):
        print "helllooo"
