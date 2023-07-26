from django.contrib import admin
from .models import Article, Comment, LikeForArticle, SubComment
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(SubComment)
admin.site.register(LikeForArticle)