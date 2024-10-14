from django.urls import path
from .views import article_create, article_edit, article_delete, about_us, article_list  # Asegúrate de importar todas las vistas necesarias
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', article_list, name='article_list'),  # URL para la lista de artículos
    path('articles/', article_list, name='article_list'),
    path('about/', about_us, name='about_us'),  # URL para la página "About Us"
    path('article/create/', article_create, name='article_create'),  # URL para crear un artículo
    path('article/edit/<slug:slug>/', article_edit, name='article_edit'),  # URL para editar un artículo
    path('article/delete/<slug:slug>/', article_delete, name='article_delete'),  # URL para eliminar un artículo
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Sirve archivos de medios
