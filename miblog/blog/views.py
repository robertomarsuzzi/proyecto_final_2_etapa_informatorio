from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Category
from .forms import CommentForm, ArticleForm, SignUpForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.db import IntegrityError
import uuid

def home(request):
    articles = Article.objects.order_by('-published_date')
    paginator = Paginator(articles, 10)  # Show 10 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'articles': articles
    }
    return render(request, 'blog/home.html', context)



def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = article.comments.all().order_by('-created_at')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.author = request.user
            new_comment.save()
            return redirect('article_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/article_detail.html', context)

@login_required
def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)  # Asegúrate de que el slug se pase aquí
    if request.user != article.author:
        return redirect('home')  # Solo el autor puede editar sus artículos

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Crea el formulario con los datos del artículo
        if form.is_valid():
            article = form.save(commit=False)  # Guarda el artículo sin confirmar
            article.slug = slugify(article.title)  # Genera un nuevo slug basado en el título
            article.save()  # Guarda el artículo en la base de datos
            return redirect('article_detail', slug=article.slug)  # Redirige a la página de detalles del artículo
    else:
        form = ArticleForm(instance=article)  # Carga el formulario con los datos del artículo existente

    context = {
        'form': form,
        'article': article  # Pasa el artículo al contexto para la plantilla
    }
    return render(request, 'blog/article_form.html', context)  # Renderiza la plantilla del formulario





def category_detail(request):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category, is_published=True)
    context = {
        'category': category,
        'articles': articles
    }
    return render(request, 'blog/category_detail.html', context)



def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = tag.articles.filter(is_published=True)
    context = {
        'tag': tag,
        'articles': articles
    }
    return render(request, 'blog/tag_detail.html', context)


@login_required
def article_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')  # Solo colaboradores pueden crear artículos
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Asegúrate de incluir request.FILES
        if form.is_valid():
            article = form.save()
            article.author = request.user  # Asignar el autor
            article.slug = slugify(article.title)
            if not article.slug:
                article.slug = str(uuid.uuid4())
            article.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'blog/article_form.html', context)

@login_required

def article_delete(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user != article.author:
        return redirect('home')  # Solo el autor puede eliminar su artículo
    
    if request.method == 'POST':
        article.delete()
        return redirect('home')

    context = {
        'article': article
    }
    return render(request, 'blog/article_confirm_delete.html', context)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')  # o cualquier otra página a la que quieras redirigir después del cierre de sesión

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'
    
    
    def get_queryset(self):
        queryset = Article.objects.all()
        category = self.request.GET.get('category')
        order = self.request.GET.get('order')
        alphabet = self.request.GET.get('alphabet')

        # Filtra por categoría si se seleccionó una
        if category:
            queryset = queryset.filter(category__slug=category)

        # Ordena por antigüedad
        if order == 'asc':
            queryset = queryset.order_by('published_date')  # Ascendente
        elif order == 'desc':
            queryset = queryset.order_by('-published_date')  # Descendente

        # Ordena alfabéticamente
        if alphabet == 'asc':
            queryset = queryset.order_by('title')  # A-Z
        elif alphabet == 'desc':
            queryset = queryset.order_by('-title')  # Z-A

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Asegúrate de tener las categorías disponibles
        return context
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'  # Ruta a la plantilla de detalle
    context_object_name = 'article'

@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            try:
                article.save()
                return redirect(article.get_absolute_url())
            except IntegrityError:
                # Si hay un error de integridad (por ejemplo, slug duplicado), 
                # genera un nuevo slug único
                article.slug = slugify(uuid.uuid4())
                article.save()
                return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

def about_us(request):
    return render(request, 'blog/about_us.html')  # Renderiza la plantilla about_us.html

def article_list(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(is_published=True)  # Filtra los artículos publicados

    # Filtrar por categoría
    category_slug = request.GET.get('category')
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    # Filtrar por antigüedad
    order = request.GET.get('order')
    if order == 'asc':
        articles = articles.order_by('published_date')  # Antigüedad ascendente
    elif order == 'desc':
        articles = articles.order_by('-published_date')  # Antigüedad descendente

    # Filtrar por orden alfabético
    alphabet_order = request.GET.get('alphabet')
    if alphabet_order == 'asc':
        articles = articles.order_by('title')  # Orden alfabético ascendente
    elif alphabet_order == 'desc':
        articles = articles.order_by('-title')  # Orden alfabético descendente
        
        
    context = {
        'articles': articles,
        'categories': categories,
    }
    return render(request, 'blog/article_list.html', context)  # Renderiza la plantilla con los artículos

def some_view(request):
    context = {
        'user': request.user,
    # Otras variables de contexto
    }
    return render(request, 'blog/base.html', context)
