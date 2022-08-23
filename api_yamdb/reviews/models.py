from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from titles.models import Title

User = get_user_model()


class PubDateModel(models.Model):
    """Abstract model for pub date."""

    pub_date = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        abstract = True


class Review(PubDateModel):
    """Review model class."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, verbose_name='Произведение')
    text = models.TextField('Текст')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    score = models.PositiveSmallIntegerField(
        'Оценка',
        max_length=2,
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        default_related_name = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                name='unique_title_author',
                fields=('title', 'author'),
            ),
        ]


    def __str__(self):
        return self.text


class Comment(PubDateModel):
    """Comment model class."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, verbose_name='Отзыв')
    text = models.TextField('Текст')

    class Meta:
        ordering = ['-pub_date']
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author} - {self.text}'
