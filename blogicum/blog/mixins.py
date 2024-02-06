from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import CommentForm, PostForm
from .models import Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        return self.get_object().author == self.request.user


class PostMixin(OnlyAuthorMixin, LoginRequiredMixin):
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


class CommentMixin(LoginRequiredMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )
