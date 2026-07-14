from django.urls import path
# Dodaliśmy MatchChatView do importów!
from .views import MatchListView, MatchDetailView, trigger_fetch, AddAnalysisView, MatchChatView

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'), 
    
    # Ścieżka do wysyłania analiz dla konkretnego meczu
    path('matches/<int:match_id>/add_analysis/', AddAnalysisView.as_view(), name='add-analysis'),
    
    # Ścieżka do aktualizacji meczów
    path('trigger-fetch/', trigger_fetch, name='trigger_fetch'), 
    
    # Ścieżka do czatu (poprawiony url, bez dublowania 'api/')
    path('matches/<int:match_id>/chat/', MatchChatView.as_view(), name='match-chat'),
]