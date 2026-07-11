from django.urls import path
# Dodajemy AddAnalysisView do importów
from .views import MatchListView, MatchDetailView, trigger_fetch, AddAnalysisView

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'), 
    
    # Ścieżka do wysyłania analiz dla konkretnego meczu
    path('matches/<int:match_id>/add_analysis/', AddAnalysisView.as_view(), name='add-analysis'),
    
    # Ścieżka do aktualizacji meczów
    path('trigger-fetch/', trigger_fetch, name='trigger_fetch'), 
]