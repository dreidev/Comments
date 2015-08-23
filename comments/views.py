from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from .models import Comment
from .forms import CommentForm
# from django.contrib.auth import authenticate, login, logout


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
            html = render_to_string(
                "comments/comment.html",
                {'object': self.object,
                 'user': self.request.user,
                 'form': CommentForm()})
            try:
                data = {
                    'success': 1,
                    'html': html,
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
    Class that lists all instances of model:comment.Comment
    """
    model = Comment
    template_name = "comments/comments.html"

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        # username = 'rana'
        # password = 'pass'
        # user = authenticate(username=username, password=password)
        # if user:
        #     login(self.request, user)
        # logout(self.request)
        return context


class CommentCreateView(AjaxableResponseMixin, CreateView):
    """
    Class that creates an instance of model:comment.Comment

    """
    form_class = CommentForm
    model = Comment
    template_name = 'comments/comment_form.html'
    success_url = reverse_lazy('comment-list')


class CommentDeleteView(DeleteView):
    """
    Class that deletes an instance of model:comment.Comment

    """
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
            if (self.object.user.id == request.user.id):
                self.object.delete()
                data = {"success": "1"}
            else:
                data = {"success": "0"}
        except:
            data = {"success": "0"}
        if request.is_ajax():
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(self.success_url)


class CommentUpdateView(AjaxableResponseMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    template_name = 'comments/edit.html'
    success_url = reverse_lazy('comment-list')
