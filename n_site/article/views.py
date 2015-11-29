# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from django.utils import timezone
from .forms import *
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
import hashlib, random

def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')[:10]
    categories = Category.objects.all()
    user = auth.get_user(request)
    context = {'latest_articles_list': latest_articles_list, 'categories':categories,'user':user, }
    if user.is_anonymous():
        return render(request, 'article/index.html', context)
    else:
        was_read_mes_set = PrivateMessage.objects.filter(reciever=user, was_read=False)
        new_message_numb = was_read_mes_set.count()
        context['new_message_numb'] = new_message_numb
        context['new_message'] = was_read_mes_set
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
                         comment_pub_date=timezone.now(), article=cur_article, author_id=user.id,)
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
    context["form"] = RegistrationForm()
    if request.method =='POST':
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data["username"],
                                                            password=newuser_form.cleaned_data["password2"],
                                                            email=newuser_form.cleaned_data["email"],
                                                            )
            newuser.is_active = False
            newuser.save()
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            salted_username = salt + newuser.username
            activation_key = hashlib.sha1(salted_username.encode('utf-8')).hexdigest()
            new_profile = UserProfile(user=newuser, activation_key=activation_key)
            new_profile.save()
            email_subject = 'Подтверждение регистрации'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link  \
                                 http://127.0.0.1:8000/article/confirm/%s" % (newuser.username, activation_key)

            send_mail(email_subject, email_body, 'email@email', [newuser.email],
                                 fail_silently=False)

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


def profile(request, user_id):
    cur_user = User.objects.get(pk=user_id)
    message_set = PrivateMessage.objects.filter(reciever=cur_user)
    was_read_mes_set = PrivateMessage.objects.filter(reciever=cur_user, was_read=True)
    not_read_mes_set = PrivateMessage.objects.filter(reciever=cur_user, was_read=False)
    context = {}
    com_set = Comment.objects.filter(com_nickname=cur_user.username)
    numb_of_comments = com_set.count()
    numb_of_likes = 0
    message_form = MessageForm()
    for comment in com_set:
        numb_of_likes += comment.c_likes_number
    context["profile_owner"] = cur_user
    context["message_set"] = message_set
    context["leaved_comments_number"] = numb_of_comments
    context["like_number"] = numb_of_likes
    context["message_form"] = message_form
    context["was_read_mes_set"] = was_read_mes_set
    context["not_read_mes_set"] = not_read_mes_set
    return render(request, 'article/profile.html', context)

def  send_message(request, reciever_id):
    cur_reciever = User.objects.get(pk=reciever_id)
    cur_user = auth.get_user(request)
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            text = message_form.cleaned_data['text']
            title = message_form.cleaned_data['title']
            mes = PrivateMessage.objects.create(author=cur_user, reciever=cur_reciever,
                         was_send=timezone.now(), header=title, message=text, was_read=False)
            mes.save()
    return HttpResponseRedirect(reverse('article:profile', args=(reciever_id)))

def show_message(request, message_id):
    message = PrivateMessage.objects.get(pk=message_id)
    context = {}
    context["message"] = message
    message.was_read = True
    message.save()
    return render(request, 'article/message.html', context)

def confirm(request, activation_key):
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    user = user_profile.user
    user.is_active = True
    user.save()
    return redirect("/article/")