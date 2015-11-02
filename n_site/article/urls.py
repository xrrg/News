from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<article_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new_post', views.new_post),
    url(r'^like_post/(?P<article_id>[0-9]+)/$', views.like_post, name='like_post'),
    url(r'^add_comment/(?P<article_id>[0-9]+)/$', views.add_comment, name='add_comment'),
    url(r'^like_comment/(?P<article_id>[0-9]+)/(?P<comment_id>[0-9]+)/$', views.like_comment, name='like_comment'),
    url(r'^by_category/(?P<category_id>[0-9]+)/', views.by_category, name='by_category'),
    #url(r'^register', views.RegisterFormView.as_view(), name="register"),
    url(r'^register', views.register, name="register"),
    url(r'^log_out', views.log_out, name="logout"),
    url(r'^log_in', views.log_in, name="login"),
]