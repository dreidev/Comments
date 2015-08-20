from django.views.generic import (
    CreateView, ListView, DeleteView, FormView)
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from .models import Comment, Like
from .forms import CommentForm


# Create your views here.
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
            try:
                pk = self.recipe_id
                data = {
                    'success': 1,
                    'pk': pk

                }
            except:
                data = {
                    'success': 1,
                }
            return JsonResponse(data)
        else:
            return response


class CommentListView(ListView):

    """
    """
    model = Comment
    template_name = "comments/comments.html"

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class CommentCreateView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_form.html'
    success_url = reverse_lazy('comment-list')


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('comment-list')

    def get(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        try:
            id = request.GET['id']
            self.object = Comment.objects.get(id=id)
            self.object.delete()
            data = {"success": "1"}
        except:
            data = {"success": "0"}
        if request.is_ajax():
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(self.success_url)


class LikeComment(FormView):

    def get(self, request, *args, **kwargs):
        comment_id = request.GET['comment_id']
        likes_count = 0
        data = {}
        try:
            user = request.user
        except:
            data['success'] = 0
            data['error'] = "You have to sign in first"
            return JsonResponse(data)
        try:
            comment = Comment.objects.get(id=comment_id)
            likes_count = comment.likes_count
            try:
                Like.objects.get(comment=comment, user=user)
                data['success'] = 0
                data['error'] = "You have already liked this comment"
            except:
                Like.objects.create(comment=comment, user=user).save()
                likes_count += 1
                comment.likes_count = likes_count
                comment.save()
                data['likes_count'] = likes_count
                data['success'] = 1
        except:
            data['error'] = "This comment might have been removed"
        return JsonResponse(data)
