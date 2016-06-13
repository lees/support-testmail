from django.conf.urls import url,include
from django.contrib import admin
admin.autodiscover()
import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^accounts/register', views.register, name='register'),
    #url(r'^accounts/logout', views.logoutview, name='logout'),
    url(r'^accounts/password_reset/done', auth_views.password_reset_done, name='password-reset-done'),
    url(r'^accounts/password_reset', auth_views.password_reset, name='password-reset'),
    #url(r'^accounts/login', views.logout, name='logout'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    #url(r'^', include('django.contrib.auth.urls')),
    #url(r'^accounts/login/$', auth_views.login),
    url(r'^admin/?', admin.site.urls),
    url(r'^$', views.root, name='home'),
    url(r'^issues/?$', views.issues, name='issues'),
    url(r'^issue/(?P<pk>[0-9]+)/?$', views.issue, name='issue'),
    url(r'^create_issue/?$', views.create_issue, name='create-issue'),
    url(r'^response_issue/?$', views.response_issue, name='response-issue'),
]
