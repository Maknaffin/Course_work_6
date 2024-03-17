from django.db import models

from service.models import NULLABLE


class Blog(models.Model):
    article_name = models.CharField(max_length=30, verbose_name='Заголовок')
    contents = models.TextField(verbose_name='Содержимое статьи')
    publication_date = models.DateField(auto_now=False, auto_now_add=False,
                                        verbose_name='Дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    image = models.ImageField(upload_to='blog/', verbose_name="Фото", **NULLABLE)

    def __str__(self):
        return f'{self.article_name}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('article_name',)