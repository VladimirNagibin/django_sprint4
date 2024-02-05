from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import COMMENTS_ON_LIST, POSTS_ON_LIST
from .forms import CommentForm, PostForm, ProfileForm
from .mixins import OnlyAuthorMixin, PostUpdateDeleteMixin
from .models import Category, Comment, Post, User


class PostListView(ListView):
    model = Post
    queryset = Post.objects.get_posts_comment_count().filter_posts().order_by('-pub_date')
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/index.html'


class PostDetailView(ListView):
    model = Comment
    template_name = 'blog/detail.html'
    post = None
    paginate_by = COMMENTS_ON_LIST

    def get_queryset(self):
        self.post = get_object_or_404(Post.objects.get_posts_comment_count(),
                                      pk=self.kwargs['post_id'])
        if self.post.author != self.request.user:
            self.post = get_object_or_404(Post.objects.get_posts_comment_count().filter_posts(),
                                          pk=self.kwargs['post_id'])
        return self.post.comments.select_related('author')

    # def get_object(self):
    #    self.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
    #    if self.post.author != self.request.user:
    #        self.post = self.post.filter_posts()
    #        return self.post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.post
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# class PostUpdateDeleteMixin(OnlyAuthorMixin):
#    model = Post
#    pk_url_kwarg = 'post_id'
#    template_name = 'blog/create.html'

#    def handle_no_permission(self):
#        return redirect(
#            'blog:post_detail',
#            post_id=self.kwargs['post_id']
#        )


class PostUpdateView(PostUpdateDeleteMixin, UpdateView):
    #form_class = PostForm

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(PostUpdateDeleteMixin, DeleteView):
    pass


class CommentCreateView(LoginRequiredMixin, CreateView):
    post_for_comment = None
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_for_comment = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_for_comment
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.post_for_comment
        return context


class CommentUpdateDeleteMixin(OnlyAuthorMixin):
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'


class CommentUpdateView(CommentUpdateDeleteMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteVeiw(CommentUpdateDeleteMixin, DeleteView):
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
