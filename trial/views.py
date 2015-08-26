from django.views.generic import DetailView
from trial.models import Post
from django.contrib.auth import authenticate, login, logout


class PostDetialView(DetailView):
    model = Post
    template_name = 'trial/trial.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetialView, self).get_context_data(**kwargs)
        username = 'rana'
        password = 'pass'
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        # logout(self.request)
        return context
