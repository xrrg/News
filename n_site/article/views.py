from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Article, Comment, Category, ArticleLikeList, CommentLikeList
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import *
from django.core.context_processors import csrf
from django.contrib import auth

def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:10]
    categories = Category.objects.all()
    user = auth.get_user(request)
    context = {'latest_articles_list': latest_articles_list, 'categories':categories,'user':user}
    return render(request, 'article/index.html', context)



def detail(request, article_id):

    try:
        cur_article = Article.objects.get(pk=article_id)
        rel_comment =  Comment.objects.filter(article=cur_article)
        user = auth.get_user(request)
        comment_form = CommentForm()
        context = {}
        context.update(csrf(request))
        article_not_liked_by_user = True
        # оценил ли пользователь?
        user_liked_article = ArticleLikeList.objects.filter(related_article=cur_article, user_nick=user.username)
        if user_liked_article:
            article_not_liked_by_user = False

        context = {'article_text': cur_article.article_text, "title" : cur_article.article_title,
                           'author' : cur_article.author_nickname,
                           'rel_comment' : rel_comment, 'comment_form' : comment_form,
                           'likes' : cur_article.likes_number, 'category':cur_article.category, 'id':article_id,
                           'not_liked':article_not_liked_by_user, }
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'article/detail.html', context)


def  like_post(request, article_id):
    try:
        if request.method == 'POST':
            cur_article = Article.objects.get(pk=article_id)
            user = auth.get_user(request)
            cur_article.likes_number += 1
            new_like = ArticleLikeList(related_article=cur_article, user_nick=user.username,)
            new_like.save()
            cur_article.save()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return HttpResponseRedirect(reverse('article:detail', args=(article_id,)))


def  add_comment(request, article_id):
    try:
        cur_article = Article.objects.get(pk=article_id)
        user = auth.get_user(request)
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['comment_text']
                com = Comment.objects.create(comment_text=text, com_nickname=user.username,
                         comment_pub_date=timezone.now(), article=cur_article, )
                com.save()
        else:
            comment_form = CommentForm()
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return HttpResponseRedirect(reverse('article:detail', args=(article_id,)))

def  like_comment(request, article_id, comment_id):
    try:
        if request.method == 'POST':
            cur_article = Article.objects.get(pk=article_id)
            cur_comment = Comment.objects.get(pk=comment_id)
            user = auth.get_user(request)
            # new_like = CommentLikeList(related_article=cur_article, related_comment=cur_comment,
            #                                                                                       user_nick=user.username)
            # new_like.save()
            cur_comment.c_likes_number += 1
            cur_comment.save()
    except Comment.DoesNotExist:
        raise Http404("Comment does not exist")
    return HttpResponseRedirect(reverse('article:detail', args=(article_id,)))

def by_category(request, category_id):
    cur_category = Category.objects.get(pk=category_id)
    category_articles_list = Article.objects.filter(category=cur_category)
    context = {"category_name":cur_category.category_name, 'category_articles_list' : category_articles_list,
                        }
    return render(request, 'article/by_category.html', context)

def register(request):
    context = {}
    context.update(csrf(request))
    context["form"] = UserCreationForm()
    if request.method =='POST':
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data["username"],
                                                            password=newuser_form.cleaned_data["password2"])
            auth.login(request, newuser)
            return redirect('/article/')
        else:
             context["form"] = newuser_form
    return render(request, 'article/register.html', context)


def log_out(request):
    auth.logout(request)
    return redirect('/article/')

def log_in(request):
    context = {}
    context.update(csrf(request))
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/article/')
        else:
             context["login_error"] = "Пользователь не найден"
             return render(request, 'article/log_in.html', context)
    else:
        return render(request, 'article/log_in.html', context)



