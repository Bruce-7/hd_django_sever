from django.urls import path
from . import views


urlpatterns = [
    path('players/all/', views.HomePlayersAllAPIView.as_view(), name='players_all'),
    path('players/', views.HomePlayersAPIView.as_view(), name='players'),
    path('players/upcomingchests/', views.HomePlayersUpcomingchestsAPIView.as_view(), name='players_upcomingchests'),
    path('players/battlelog/', views.HomePlayersBattlelogAPIView.as_view(), name='players_battlelog')
]
