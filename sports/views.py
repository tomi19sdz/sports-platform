import os
import time
import requests
from .utils import wygeneruj_analize_ai
from datetime import date, timedelta
from collections import defaultdict
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse, JsonResponse
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
class AddAnalysisView(APIView):
   def post(self, request, match_id):
       try:
           match = Match.objects.get(id=match_id)
           content = request.data.get('content')
           if not content:
               return Response({"error": "Brak treści"}, status=status.HTTP_400_BAD_REQUEST)
           Analysis.objects.create(match=match, content=content)
           return Response({"message": "Dodano"}, status=status.HTTP_201_CREATED)
       except Match.DoesNotExist:
           return Response({"error": "Brak meczu"}, status=status.HTTP_404_NOT_FOUND)
class MatchChatView(APIView):
   def get(self, request, match_id):
       messages = ChatMessage.objects.filter(match_id=match_id).order_by('created_at')
       data = [{"id": msg.id, "author": msg.author, "text": msg.text} for msg in messages]
       return Response(data)
   def post(self, request, match_id):
       try:
           match = Match.objects.get(id=match_id)
       except Match.DoesNotExist:
           return Response({"error": "Mecz nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
       author = request.data.get('author', 'Anonim')
       text = request.data.get('text')
       if not text:
           return Response({"error": "Brak tekstu."}, status=status.HTTP_400_BAD_REQUEST)
       new_message = ChatMessage.objects.create(match=match, author=author, text=text)
       return Response({"id": new_message.id, "author": new_message.author, "text": new_message.text}, status=status.HTTP_201_CREATED)
def trigger_fetch(request):
   token = request.GET.get('token')
   if token != 'moje-tajne-haslo-123':
       return HttpResponse("Brak dostępu", status=403)
   api_key_raw = os.environ.get('FOOTBALL_DATA_KEY')
   if not api_key_raw:
       return HttpResponse("Błąd: Brak klucza FOOTBALL_DATA_KEY w pliku .env na serwerze.", status=500)
   api_key = api_key_raw.strip()
   headers = {
       'X-Auth-Token': api_key
   }
   # Słownik mapujący kody lig na pełne, czytelne nazwy zapisywane w bazie
   nazwy_lig = {
       'WC': 'FIFA World Cup',
       'CL': 'UEFA Champions League',
       'BL1': 'Bundesliga',
       'DED': 'Eredivisie',
       'PD': 'La Liga',
       'FL1': 'Ligue 1',
       'ELC': 'Championship',
       'PPL': 'Primeira Liga',
       'EC': 'European Championship',
       'SA': 'Serie A',
       'PL': 'Premier League'
   }
   znalezione_mecze = 0
   dzisiaj = date.today()
   data_koncowa = dzisiaj + timedelta(days=3)
   raport = f"<b>Raport z pobierania (Z nazwami lig - Od {dzisiaj} do {data_koncowa}):</b><br><br>"
   for kod_ligi, pelna_nazwa_ligu in nazwy_lig.items():
       url = f'https://api.football-data.org/v4/competitions/{kod_ligi}/matches?dateFrom={dzisiaj}&dateTo={data_koncowa}'
       try:
           response = requests.get(url, headers=headers)
           if response.status_code == 200:
               data = response.json()
               matches = data.get('matches', [])
               raport += f"- Liga <b>{pelna_nazwa_ligu}</b>: Znaleziono {len(matches)} meczów.<br>"
               for m in matches:
                   home_team = m.get('homeTeam', {}).get('name')
                   away_team = m.get('awayTeam', {}).get('name')
                   match_date = m.get('utcDate')
                   status_val = m.get('status')
                   score_info = m.get('score', {}).get('fullTime', {})
                   home_score = score_info.get('home')
                   away_score = score_info.get('away')
                   if not home_team or not away_team or not match_date:
                       continue
                   if status_val == 'FINISHED':
                       mapped_status = 'FINISHED'
                   elif status_val in ['IN_PLAY', 'PAUSED']:
                       mapped_status = 'IN_PLAY'
                   else:
                       mapped_status = 'SCHEDULED'
                   # Zapisujemy mecz wraz z przypisaną nazwą ligi
                   Match.objects.update_or_create(
                       home_team=home_team,
                       away_team=away_team,
                       match_date=parse_datetime(match_date),
                       defaults={
                           'home_logo': m.get('homeTeam', {}).get('crest', ''),
                           'away_logo': m.get('awayTeam', {}).get('crest', ''),
                           'home_score': home_score,
                           'away_score': away_score,
                           'status': mapped_status,
                           'league': pelna_nazwa_ligu  # <--- Przypisanie dokładnej nazwy ligi
                       }
                   )
                   znalezione_mecze += 1
           elif response.status_code == 403:
               raport += f"- Liga <b>{pelna_nazwa_ligu}</b>: Brak dostępu w planie darmowym.<br>"
           else:
               raport += f"- Liga <b>{pelna_nazwa_ligu}</b>: Kod {response.status_code}<br>"
       except Exception as e:
           raport += f"- Liga {pelna_nazwa_ligu}: Błąd - {e}<br>"
       time.sleep(15)
   raport += f"<br><b>Zakończono! Zaktualizowano w bazie łącznie {znalezione_mecze} meczów.</b>"
   return HttpResponse(raport)
def api_generuj_analize(request):
   mecz = request.GET.get('mecz')
   if not mecz:
       return JsonResponse({'blad': 'Nie podano nazwy meczu.'}, status=400)
   try:
       gotowa_analiza = wygeneruj_analize_ai(mecz)
       return JsonResponse({
           'mecz': mecz,
           'analiza': gotowa_analiza
       })
   except Exception as e:
       return JsonResponse({'blad': f'Wystąpił błąd: {str(e)}'}, status=500)