from django import forms
from .models import Article, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Campo que se incluirá en el formulario de comentario
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),  # Campo de texto para el contenido del comentario
        }




class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # Modelo asociado al formulario
        fields = ['title', 'content', 'category', 'image']  # Campos que se incluirán en el formulario
        exclude = ['published_date', 'author', 'slug']  # Campos que se excluirán del formulario


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
