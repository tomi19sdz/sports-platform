import requests
from datetime import date, timedelta
from collections import defaultdict
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from .models import Match, Analysis, ChatMessage
from .serializers import MatchSerializer

class MatchListView(ListAPIView):
    queryset = Match.objects.all().order_by('match_date')
    serializer_class = MatchSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        grouped_matches = defaultdict(list)
        for match in serializer.data:
            date_key = match['match_date'].split('T')[0]
            grouped_matches[date_key].append(match)
        return Response(grouped_matches)

class MatchDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

# Widoki dodawania analiz i czatu (bez zmian)
class AddAnalysisView(APIView):
    def post(self, request, match_id):
        content = request.data.get('content')
        if not content: return Response({"error": "Pusta treść"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            match = Match.objects.get(id=match_id)
            Analysis.objects.create(match=match, content=content)
            return Response({"message": "Dodano"}, status=status.HTTP_201_CREATED)
        except Match.DoesNotExist: return Response({"error": "Brak meczu"}, status=status.HTTP_404_NOT_FOUND)

class MatchChatView(APIView):
    def get(self, request, match_id):
        messages = ChatMessage.objects.filter(match_id=match_id).order_by('created_at')
        return Response([{"id": msg.id, "author": msg.author, "text": msg.text} for msg in messages])
    def post(self, request, match_id):
        try:
            match = Match.objects.get(id=match_id)
            new_message = ChatMessage.objects.create(match=match, author=request.data.get('author', 'Anonim'), text=request.data.get('text'))
            return Response({"id": new_message.id, "author": new_message.author, "text": new_message.text}, status=status.HTTP_201_CREATED)
        except Match.DoesNotExist: return Response({"error": "Brak meczu"}, status=status.HTTP_404_NOT_FOUND)

def trigger_fetch(request):
    # Logika z obsługą wyniku
    headers = { 'X-Auth-Token': 'c92a85877e2c4319aea223d3543532f8' }
    url = 'https://api.football-data.org/v4/matches?competitions=WC,PL,CL,PD,BL1,DED,FL1,PPL,EC,SA'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for m in response.json().get('matches', []):
            score = m.get('score', {}).get('fullTime', {})
            Match.objects.update_or_create(
                home_team=m['homeTeam']['name'], away_team=m['awayTeam']['name'], match_date=parse_datetime(m['utcDate']),
                defaults={
                    'home_logo': m['homeTeam'].get('crest', ''), 'away_logo': m['awayTeam'].get('crest', ''),
                    'home_score': score.get('home'), 'away_score': score.get('away'), 'status': m.get('status')
                }
            )
        return HttpResponse("Wyniki zaktualizowane!")
    return HttpResponse("Błąd API", status=500)