from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .constants import POSTS_ON_LIST
from .forms import CommentForm, PostForm
from .models import Category, Comment, Post


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostListView(ListView):
    model = Post
    queryset = Post.objects.get_published_posts()
    # ordering = '-pub_date'
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/index.html'


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.get_published_posts(),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self):
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


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    post_list = category.posts.get_published_posts()

    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )


User = get_user_model()


def profile_user(request, username):
    profile = get_object_or_404(
        User,
        username=username,
    )
    page_obj = profile.posts.get_published_posts()
    return render(
        request,
        'blog/profile.html',
        {'profile': profile, 'page_obj': page_obj}
    )


class UserPostsListView(ListView):
    model = Post
    queryset = Post.objects.get_published_posts()
    # ordering = '-pub_date'
    paginate_by = POSTS_ON_LIST
    template_name = 'blog/profile.html'

    # model = User
    # slug_url_kwarg = 'username'
    # slug_field = 'username'
    # template_name = 'blog/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'],
        )
    #    context['page_obj'] = self.object.posts.get_published_posts()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# @login_required
# def add_comment(request, post_id):
#    post = get_object_or_404(Post, pk=post_id)
#    form = CommentForm(request.POST)
#    if form.is_valid():
#        comment = form.save(commit=False)
#        comment.author = request.user
#        comment.post = post
#        comment.save()
#    return redirect('blog:post_detail', post_id=post_id)


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

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.post_for_comment.pk}
        )


class CommentMixin:
    model = Comment
    pk_url_kwarg = 'comment_id'
    template_name = 'blog/comment.html'

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class CommentUpdateView(CommentMixin, OnlyAuthorMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteVeiw(CommentMixin, OnlyAuthorMixin, DeleteView):
    pass
