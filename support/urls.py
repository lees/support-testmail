"""support URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
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
    url(r'^issue/([0-9]+)/?$', views.issue, name='issue'),
    url(r'^create_issue/?$', views.create_issue, name='create-issue'),
]
