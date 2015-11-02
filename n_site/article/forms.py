from .models import Article, Comment, Category
from django.core.urlresolvers import reverse
from django import forms
from django.utils import timezone
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login



class PostForm(forms.Form):
	post_title = forms.CharField(label='Article title', max_length=100)
	post_text = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    comment_text = forms.CharField(label='Текст ', widget=forms.Textarea)