from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView
)

from .constants import COMMENTS_ON_LIST, POSTS_ON_LIST
from .forms import CommentForm, PostForm, ProfileForm
from .mixins import CommentMixin, OnlyAuthorMixin, PostMixin
from .models import Category, Comment, Post, User


class PostListView(ListView):
    model = Post
    queryset = Post.objects.get_posts_comment_count().filter_posts()
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/index.html'


class PostDetailView(ListView):
    model = Comment
    template_name = 'blog/detail.html'
    paginate_by = COMMENTS_ON_LIST

    def get_object(self):
        post = get_object_or_404(
            Post.objects.get_posts_comment_count(),
            pk=self.kwargs['post_id']
        )
        if post.author != self.request.user:
            post = get_object_or_404(
                Post.objects.get_posts_comment_count().filter_posts(),
                pk=self.kwargs['post_id']
            )
        return post

    def get_queryset(self):
        return self.get_object().comments.select_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(PostMixin, UpdateView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, DeleteView):
    pass


class CommentCreateView(CommentMixin, CreateView):
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    pass


class CommentDeleteVeiw(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass


class CategoryPostsListView(ListView):
    model = Post
    category = None
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/category.html'

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return self.get_category().posts.get_posts_comment_count(
        ).filter_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class UserPostsListView(ListView):
    model = Post
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/profile.html'

    def get_profile(self):
        return get_object_or_404(
            User,
            username=self.kwargs['username'],
        )

    def get_queryset(self):
        profile = self.get_profile()
        posts = profile.posts.get_posts_comment_count()
        if profile == self.request.user:
            return posts
        return posts.filter_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
