import requests
from datetime import date, timedelta
from collections import defaultdict

from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView # NOWY IMPORT
from rest_framework.response import Response
from rest_framework import status # NOWY IMPORT

# Zaktualizowany import - dodano Analysis
from .models import Match, Analysis
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

# ==========================================
# WIDOK DO DODAWANIA ANALIZ (NOWE)
# ==========================================
class AddAnalysisView(APIView):
    def post(self, request, match_id):
        # 1. Odbieramy treść wpisaną przez użytkownika
        content = request.data.get('content')
        
        if not content:
            return Response({"error": "Treść analizy nie może być pusta."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Szukamy odpowiedniego meczu i przypisujemy do niego analizę
        try:
            match = Match.objects.get(id=match_id)
            Analysis.objects.create(match=match, content=content)
            return Response({"message": "Analiza dodana pomyślnie!"}, status=status.HTTP_201_CREATED)
        except Match.DoesNotExist:
            return Response({"error": "Podany mecz nie istnieje."}, status=status.HTTP_404_NOT_FOUND)

# ==========================================
# FUNKCJA DO AUTOMATYZACJI POBIERANIA (WEBHOOK)
# ==========================================
def trigger_fetch(request):
    # 1. Weryfikacja hasła
    token = request.GET.get('token')
    if token != 'moje-tajne-haslo-123':
        return HttpResponse("Brak dostępu", status=403)
    
    # 2. Twoja logika pobierająca
    headers = { 'X-Auth-Token': 'c92a85877e2c4319aea223d3543532f8' }
    
    dzisiaj = date.today()
    kolejne_dni = dzisiaj + timedelta(days=3)
    
    date_from = dzisiaj.strftime('%Y-%m-%d')
    date_to = kolejne_dni.strftime('%Y-%m-%d')
    
    wybrane_ligi = "WC,PL,CL,PD,BL1,DED,FL1,PPL,EC,SA"
    url = f'https://api.football-data.org/v4/matches?competitions={wybrane_ligi}&dateFrom={date_from}&dateTo={date_to}'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
            
            dodano = 0
            zaktualizowano = 0
            
            for m in matches:
                home_team = m.get('homeTeam')
                away_team = m.get('awayTeam')
                
                if home_team and away_team and home_team.get('name') and away_team.get('name'):
                    home = home_team['name']
                    away = away_team['name']
                    match_date = parse_datetime(m.get('utcDate'))
                    
                    home_crest = home_team.get('crest', '')
                    away_crest = away_team.get('crest', '')
                    
                    match, created = Match.objects.update_or_create(
                        home_team=home,
                        away_team=away,
                        match_date=match_date,
                        defaults={
                            'home_logo': home_crest,
                            'away_logo': away_crest
                        }
                    )
                    if created:
                        dodano += 1
                    else:
                        zaktualizowano += 1
                        
            # Zwracamy podsumowanie na ekran (zamiast do konsoli)
            return HttpResponse(
                f"Sukces! Sprawdzono: {date_from} do {date_to}. "
                f"Dodano {dodano} nowych, zaktualizowano {zaktualizowano} istniejących."
            )
        else:
            return HttpResponse(f"Błąd API: {response.status_code}", status=500)
            
    except Exception as e:
        return HttpResponse(f"Wystąpił błąd: {e}", status=500)