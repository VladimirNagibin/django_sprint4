from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .constants import TITLE_MAX_LENGTH, PRESENTATION_MAX_LENGTH
from core.models import IsPublishedCreatedAtModel

User = get_user_model()


class Category(IsPublishedCreatedAtModel):
    title = models.CharField('Заголовок', max_length=TITLE_MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        ),
    )

    class Meta(IsPublishedCreatedAtModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:PRESENTATION_MAX_LENGTH]


class Location(IsPublishedCreatedAtModel):
    name = models.CharField('Название места', max_length=TITLE_MAX_LENGTH)

    class Meta(IsPublishedCreatedAtModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:PRESENTATION_MAX_LENGTH]


class PublishedManager(models.QuerySet):
    def get_published_posts(self):
        return self.select_related(
            'category', 'location', 'author'
        ).filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        )


class Post(IsPublishedCreatedAtModel):
    title = models.CharField('Заголовок', max_length=TITLE_MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)
    objects = PublishedManager.as_manager()

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:PRESENTATION_MAX_LENGTH]

    def get_absolute_url(self):
        return reverse('post:profile', kwargs={'username': self.username})


class Comment(models.Model):
    text = models.TextField('Комментарий')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta:
        ordering = ('created_at',)
        default_related_name = 'comments'
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
