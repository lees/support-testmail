from django.conf.urls import url,include
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    #url(r'^accounts/login/$', auth_views.login),
    url(r'^admin/?', admin.site.urls),
    url(r'^$', views.root, name='home'),
    url(r'^my_issues/?$', views.my_issues, name='my-issues'),
    url(r'^unresolved_issues/?$', views.unresolved_issues, name='unresolved-issues'),
    #url(r'^issue/([0-9]+)/?$', views.issue, name='issue'),
    url(r'^issue/(?P<pk>[0-9]+)/?$', views.IssueView.as_view(), name='issue'),
    url(r'^create_issue/?$', views.create_issue, name='create-issue'),
]
