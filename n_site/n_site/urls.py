from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    #nurl(r'^$', 'n_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^article/', include('article.urls', namespace="article")),
    #url(r'^register/$', views.RegisterFormView.as_view()),
)