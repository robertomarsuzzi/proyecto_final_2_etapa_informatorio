"""
URL configuration for miblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from blog import views
from django.contrib.auth import views as auth_views
from blog.views import ArticleListView

from django.contrib.auth.decorators import login_required
from blog.views import about_us

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Asegúrate de incluir las URLs de la aplicación blog
    path('', views.home, name='home'),
    path('article/create/', views.article_create, name='article_create'),  # Mueve esta línea antes de article_detail
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'),
    path('article/<slug:slug>/edit/', views.article_edit, name='article_edit'),
    path('article/<slug:slug>/delete/', views.article_delete, name='article_delete'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
   
     #path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('about/', about_us, name='about_us'),  # Agrega la URL para la página About Us
]

def dashboard(request):
    return render(request, 'blog/dashboard.html')

#if settings.DEBUG:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Sirve archivos de medios
    