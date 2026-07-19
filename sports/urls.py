from django.urls import path
from .views import MatchListView, MatchDetailView, trigger_fetch, AddAnalysisView, MatchChatView, api_generuj_analize

urlpatterns = [
    path('matches/', MatchListView.as_view(), name='match-list'),
    path('matches/<int:pk>/', MatchDetailView.as_view(), name='match-detail'), 
    path('matches/<int:match_id>/add_analysis/', AddAnalysisView.as_view(), name='add-analysis'),
    path('trigger-fetch/', trigger_fetch, name='trigger_fetch'), 
    path('matches/<int:match_id>/chat/', MatchChatView.as_view(), name='match-chat'),
    
    # Zmieniona ścieżka - usunęliśmy "api/" z początku:
    path('generuj-analize/', api_generuj_analize, name='api_generuj_analize'),
]