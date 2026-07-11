from django.urls import path
from .views import MatchListView, MatchDetailView, trigger_fetch

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'), 
    
    # NOWA ŚCIEŻKA DO AKTUALIZACJI MECZÓW
    path('trigger-fetch/', trigger_fetch, name='trigger_fetch'), 
]