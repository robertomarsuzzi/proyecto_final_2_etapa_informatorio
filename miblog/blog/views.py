from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import CommentForm, ArticleForm

def home(request):
    articles = Article.objects.filter(is_published=True).order_by('-published_date')
    context = {
        'articles': articles
    }
    return render(request, 'blog/home.html', context)



def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    comments = Comment.objects.filter(article=article, is_approved=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    else:
        form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/article_detail.html', context)

def article_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    
    if request.user != article.author:
        return redirect('home')  # Solo el autor puede editar sus artículos

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article
    }
    return render(request, 'blog/article_form.html', context)





def category_detail(request, slug):
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



def article_create(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('home')  # Solo colaboradores pueden crear artículos
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()

    context = {
        'form': form
    }
    return render(request, 'blog/article_form.html', context)


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