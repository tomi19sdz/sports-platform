import requests
from datetime import date, timedelta
from collections import defaultdict
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView
<<<<<<< Updated upstream
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
=======
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
=======
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

>>>>>>> Stashed changes
def trigger_fetch(request):
    token = request.GET.get('token')
    if token != 'moje-tajne-haslo-123':
        return HttpResponse("Brak dostępu", status=403)
<<<<<<< Updated upstream

    headers = { 'X-Auth-Token': 'c92a85877e2c4319aea223d3543532f8' }

=======

    headers = { 'X-Auth-Token': 'c92a85877e2c4319aea223d3543532f8' }

>>>>>>> Stashed changes
    # --- KLUCZOWA ZMIANA: Zmuszamy API do sprawdzania 7 dni wstecz ---
    dzisiaj = date.today()
    tydzien_temu = dzisiaj - timedelta(days=7)
    kolejne_dni = dzisiaj + timedelta(days=3)
<<<<<<< Updated upstream

=======

>>>>>>> Stashed changes
    date_from = tydzien_temu.strftime('%Y-%m-%d')
    date_to = kolejne_dni.strftime('%Y-%m-%d')

    wybrane_ligi = "WC,PL,CL,PD,BL1,DED,FL1,PPL,EC,SA"
    url = f'https://api.football-data.org/v4/matches?competitions={wybrane_ligi}&dateFrom={date_from}&dateTo={date_to}'

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = data.get('matches', [])
<<<<<<< Updated upstream

=======

>>>>>>> Stashed changes
            for m in matches:
                home_team = m.get('homeTeam')
                away_team = m.get('awayTeam')

                if home_team and away_team and home_team.get('name') and away_team.get('name'):
                    # Pobieranie wyniku z API
                    score = m.get('score', {}).get('fullTime', {})
<<<<<<< Updated upstream

                    Match.objects.update_or_create(
                        home_team=home_team['name'],
                        away_team=away_team['name'],
                        match_date=parse_datetime(m['utcDate']),
                        defaults={
                            'home_logo': home_team.get('crest', ''),
                            'away_logo': away_team.get('crest', ''),
                            'home_score': score.get('home'),
                            'away_score': score.get('away'),
=======

                    Match.objects.update_or_create(
                        home_team=home_team['name'],
                        away_team=away_team['name'],
                        match_date=parse_datetime(m['utcDate']),
                        defaults={
                            'home_logo': home_team.get('crest', ''),
                            'away_logo': away_team.get('crest', ''),
                            'home_score': score.get('home'),
                            'away_score': score.get('away'),
>>>>>>> Stashed changes
                            'status': m.get('status')
                        }
                    )
            return HttpResponse(f"Sukces! Pobrano wyniki od {date_from} do {date_to}.")
        return HttpResponse(f"Błąd API: {response.status_code}", status=500)
    except Exception as e:
        return HttpResponse(f"Wystąpił błąd: {e}", status=500)