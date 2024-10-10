from django.contrib import admin
from .models import Article, Category, Comment, Tag

admin.site.register(Article)  # Registra el modelo Article en el panel de administración
admin.site.register(Category)  # Registra el modelo Category en el panel de administración
admin.site.register(Comment)  # Registra el modelo Comment en el panel de administración
admin.site.register(Tag)  # Registra el modelo Tag en el panel de administración


# Register your models here.
