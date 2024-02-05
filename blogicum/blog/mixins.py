from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user


class PostUpdateDeleteMixin(OnlyAuthorMixin, LoginRequiredMixin):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    form_class = PostForm

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs[self.pk_url_kwarg]
        )

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )

    #def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['form'] = PostForm
    #    return context
