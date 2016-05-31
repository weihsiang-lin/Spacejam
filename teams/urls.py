from . import views
from spacejam import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r'^myteams/$', views.myteams, name='myteams'),
    url(r'^myteams/(?P<team_id>[0-9]+)/edit/$', views.edit_team, name='edit_team'),
    url(r'^myteams/(?P<team_id>[0-9]+)/delete/$', views.delete_team, name='delete_team'),
    url(r'^myteams/(?P<team_id>[0-9]+)/summary/$', views.team_summary, name='team_summary'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/$', views.mygames, name='mygames'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/create/$', views.create_game, name='create_game'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/(?P<game_id>[0-9]+)/edit/$', views.edit_game, name='edit_game'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/(?P<game_id>[0-9]+)/edit/states/$', views.edit_game_states, name='edit_game_states'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/(?P<game_id>[0-9]+)/complete/$', views.complete_game, name='complete_game'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/(?P<game_id>[0-9]+)/complete/edit/$', views.edit_complete_game, name='edit_complete_game'),
    url(r'^myteams/(?P<team_id>[0-9]+)/games/(?P<game_id>[0-9]+)/delete/$', views.delete_game, name='delete_game'),
    url(r'^myteams/(?P<team_id>[0-9]+)/stats/', views.stats, name='stats'),
    url(r'^myteams/(?P<team_id>[0-9]+)/players/', include('players.urls')),
    url(r'^myteams/create/$', views.create_team, name='create_team'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
