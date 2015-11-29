from .models import Article, Comment, Category
from django.core.urlresolvers import reverse
from django import forms
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User




class PostForm(forms.Form):
	post_title = forms.CharField(label='Article title', max_length=100)
	post_text = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Текст ', widget=forms.Textarea)

class MessageForm(forms.Form):
    title = forms.CharField(label='Заголовок', max_length=200)
    text = forms.CharField(widget=forms.Textarea)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Электронный адрес'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')