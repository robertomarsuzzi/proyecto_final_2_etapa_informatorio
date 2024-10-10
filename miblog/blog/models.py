from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre de la categoría
    description = models.TextField(blank=True, null=True)  # Descripción opcional de la categoría
    slug = models.SlugField(max_length=100, unique=True)  # Slug único para la URL

    class Meta:
        verbose_name_plural = "Categories"  # Nombre plural para el modelo

    def __str__(self):
        return self.name  # Devuelve el nombre de la categoría como representación del objeto

class Article(models.Model):
    title = models.CharField(max_length=200)  # Título del artículo
    slug = models.SlugField(unique=True, max_length=200)  # Slug único para la URL
    content = models.TextField()  # Contenido del artículo
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Autor del artículo
    published_date = models.DateTimeField(auto_now_add=True)  # Fecha de publicación automática
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Categoría del artículo
    image = models.ImageField(upload_to='articles/', blank=True, null=True)  # Imagen del artículo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Genera el slug a partir del título
            if not self.slug:
                self.slug = str(uuid.uuid4())  # Genera un slug único si no se puede crear uno
        super().save(*args, **kwargs)  # Llama al método save de la clase base

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.slug})  # Devuelve la URL absoluta del artículo

    class Meta:
        ordering = ['-published_date']  # Ordena los artículos por fecha de publicación (más recientes primero)
        verbose_name_plural = "Articles"  # Nombre plural para el modelo

    def __str__(self):
        return self.title  # Devuelve el título del artículo como representación del objeto

class Comment(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario por {self.author.username} en {self.article.title}'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    articles = models.ManyToManyField(Article, related_name='tags')

    def __str__(self):
        return self.name