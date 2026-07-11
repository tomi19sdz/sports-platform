from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from collections import defaultdict
from django.http import HttpResponse # <-- NOWY IMPORT
from .models import Match
from .serializers import MatchSerializer

class MatchListView(ListAPIView):
    queryset = Match.objects.all().order_by('match_date')
    serializer_class = MatchSerializer

    def list(self, request, *args, **kwargs):
        # 1. Pobieramy mecze posortowane chronologicznie
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # 2. Tworzymy słownik, który automatycznie grupuje listy
        grouped_matches = defaultdict(list)
        
        for match in serializer.data:
            # match['match_date'] to np. "2026-07-09T22:00:00Z"
            # Wyciągamy samą datę (pierwsze 10 znaków: "2026-07-09")
            date_key = match['match_date'].split('T')[0]
            grouped_matches[date_key].append(match)
            
        # 3. Zwracamy pogrupowane dane
        return Response(grouped_matches)

class MatchDetailView(RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

# ==========================================
# NOWA FUNKCJA DO AUTOMATYZACJI POBIERANIA
# ==========================================
def trigger_fetch(request):
    # 1. Sprawdzamy hasło, aby nikt obcy nie zepsuł Ci bazy
    token = request.GET.get('token')
    if token != 'moje-tajne-haslo-123':
        return HttpResponse("Brak dostępu", status=403)
    
    # 2. MIEJSCE NA LOGIKĘ POBIERAJĄCĄ
    # Tutaj na razie jest pusto! Musimy napisać kod, który faktycznie 
    # połączy się z zewnętrznym źródłem i zapisze dane do bazy.
    
    return HttpResponse("Pomyślnie uruchomiono skrypt aktualizujący mecze!")