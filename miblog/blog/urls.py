from django.urls import path , include

from .views import article_create, article_edit,article_detail, ArticleListView, article_delete, about_us, article_list , ArticleDetailView # Asegúrate de importar todas las vistas necesarias
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', article_list, name='article_list'),  # URL para la lista de artículos
    path('articles/<slug:slug>', article_list, name='article_list'),
    path('about/', about_us, name='about_us'),  # URL para la página "About Us"
    path('article/create/', article_create, name='article_create'),  # URL para crear un artículo
    path('article/<slug:slug>/edit/', article_edit, name='article_edit'),  # URL para editar un artículo
    path('article/<slug:slug>/delete/', article_delete, name='article_delete'),  # URL para eliminar un artículo
    path('article/', ArticleDetailView.as_view(), name='article_list'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/', ArticleListView.as_view(), name='article_list'),  # Vista de lista
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),  # Vista de detalle
    path('tinymce/', include('tinymce.urls')),  # Añadir TinyMCE en las URLs
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Sirve archivos de medios
