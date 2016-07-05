import views

from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='player_index'),
    url(r'^create/$', views.create, name='create_player'),
    url(r'^(?P<player_id>[0-9]+)/edit/$', views.edit, name='edit_player'),
    url(r'^(?P<player_id>[0-9]+)/delete/$', views.delete, name='delete_player'),
    url(r'^(?P<player_id>[0-9]+)/summary/$', views.summary, name='player_summary'),
    url(r'^(?P<player_id>[0-9]+)/invitation/$', views.invitation, name='invitation'),
    url(r'^(?P<player_id>[0-9]+)/invitation/register/$', views.invite_registration, name='invite_registration'),
    url(r'^(?P<player_id>[0-9]+)/analytics/$', views.analytics, name='player_analytics'),
]
