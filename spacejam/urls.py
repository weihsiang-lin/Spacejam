from . import views
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/logout/$', views.logout),
    url(r'^accounts/register/$', views.register),
    url(r'^accounts/my/$', views.my_account, name='my_account'),
    url(r'^accounts/change_password/$', views.change_password, name='change_password'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^teams/', include('teams.urls')),
    url(r'^how_it_works$', views.how_it_works, name='how_it_works'),
    url(r'^privacy_policy$', views.privacy_policy, name='privacy_policy'),
    # url(r'^leagues/', include('leagues.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
