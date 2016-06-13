from django.conf.urls import url, include
from django.contrib import admin
import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/(?P<pk>[0-9]+)/?$', views.account, name='account'),
    url(r'^accounts/register', views.register, name='register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/?', admin.site.urls),
    url(r'^$', views.root, name='home'),
    url(r'^issues/?$', views.issues, name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/?$', views.issue, name='issue'),
    url(r'^create_issue/?$', views.create_issue, name='create-issue'),
    url(r'^response_issue/?$', views.response_issue, name='response-issue'),
    url(r'^issue_created/?$', views.issue_created, name='issue-created'),
]
