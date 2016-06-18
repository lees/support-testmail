from django.conf.urls import url, include
from django.contrib import admin
#import support.views as support_views
import views

urlpatterns = [
    url(r'^accounts/(?P<pk>[0-9]+)/?$', views.account, name='account'),
    url(r'^accounts/register', views.register, name='register'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/?', admin.site.urls),
    url(r'^$', views.root, name='home'),
    #url(r'^', include(support_views)),
    url(r'^', include('support.urls')),

]
