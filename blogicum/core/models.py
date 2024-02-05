from django.db import models


class CreatedAtModel(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class IsPublishedCreatedAtModel(CreatedAtModel):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta(CreatedAtModel.Meta):
        abstract = True
