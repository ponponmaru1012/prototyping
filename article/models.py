from django.db import models
from accounts.models import CustomUser
from mdeditor.fields import MDTextField
from django.utils import timezone
# Create your models here.


class Article(models.Model):

    post_user = models.ForeignKey(CustomUser, verbose_name='Post User', on_delete=models.CASCADE, related_name='name',)
    title = models.CharField(verbose_name='title', max_length=50,)
    content = MDTextField()
    thumbnail = models.ImageField(verbose_name='thumbnail', null=False, blank=False,)
    created_at = models.DateField(verbose_name='created_at', auto_now_add=True,)
    updated_at = models.DateField(verbose_name='updated_at', auto_now=True)
    view_count = models.PositiveIntegerField(verbose_name='view count', default=0,)

    class Meta:
        verbose_name_plural = 'Article'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Comment(models.Model):
    #記事に対するコメント
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    content = MDTextField()
    target = models.ForeignKey(Article, on_delete=models.CASCADE,)
    created_at = models.DateField(verbose_name='created_at', auto_now_add=True,)
    updated_at = models.DateField(verbose_name='updated_at', auto_now=True,)

    def __str__(self):
        return self.content[:20]

    class Meta:
        ordering = ['created_at']

class SubComment(models.Model):
    #コメントに対する返信
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    content = MDTextField()
    target = models.ForeignKey(Comment, on_delete=models.CASCADE,)
    created_at = models.DateField(verbose_name='created_at', auto_now_add=True,)
    updated_at = models.DateField(verbose_name='updated_at', auto_now=True,)

    def __str__(self):
        return self.content[:20]

    class Meta:
        ordering = ['created_at']


class LikeForArticle(models.Model):
    #記事に対するイイね
    target = models.ForeignKey(Article, on_delete=models.CASCADE,)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,)
    timestamp = models.DateTimeField(default=timezone.now,)