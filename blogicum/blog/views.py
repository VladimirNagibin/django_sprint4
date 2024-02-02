from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import POSTS_ON_LIST
from .forms import CommentForm, PostForm, ProfileForm
from .models import Category, Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    queryset = Post.objects.get_published_posts()
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/index.html'


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self):
        if self.request.user.id == super().get_object().author_id:
            return get_object_or_404(
                Post.objects.get_posts(),
                pk=self.kwargs['post_id']
            )
        return get_object_or_404(
            Post.objects.get_published_posts(),
            pk=self.kwargs['post_id']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostMixin(OnlyAuthorMixin):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'

    def handle_no_permission(self):
        return redirect(
            'blog:post_detail',
            post_id=self.kwargs['post_id']
        )


class PostUpdateView(PostMixin, UpdateView):
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, DeleteView):

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_for_comment = None
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        self.post_for_comment = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_for_comment
        return super().form_valid(form)


class CommentMixin(OnlyAuthorMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'


class CommentUpdateView(CommentMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteVeiw(CommentMixin, OnlyAuthorMixin, DeleteView):
    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CategoryPostsListView(ListView):
    model = Post
    category = None
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/category.html'

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return self.category.posts.get_published_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


User = get_user_model()


class UserPostsListView(ListView):
    model = Post
    profile = None
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/profile.html'

    def get_queryset(self):
        self.profile = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
        if self.profile != self.request.user:
            return self.profile.posts.get_published_posts()
        return self.profile.posts.get_posts()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.profile
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
