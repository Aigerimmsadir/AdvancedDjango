from django.contrib import admin
from main.models import *

admin.site.register(Article)

admin.site.register(ArticleImage)

admin.site.register(FavoriteArticle)