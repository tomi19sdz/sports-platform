import requests
from django.core.management.base import BaseCommand
from sports.models import Match
from django.utils.dateparse import parse_datetime
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Pobiera mecze z wybranych lig wyłącznie na dzisiaj i jutro'

    def handle(self, *args, **options):
        headers = { 'X-Auth-Token': 'c92a85877e2c4319aea223d3543532f8' }
        
        # Nowe okienko (dzisiaj + 3 dni)
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
                
                # Dwa oddzielne liczniki
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
                            zaktualizowano += 1 # Jeśli nie stworzył nowego, to go zaktualizował
                            
                self.stdout.write(self.style.SUCCESS(
                    f'Sukces! Sprawdzono: {date_from} do {date_to}. '
                    f'Dodano {dodano} nowych, zaktualizowano {zaktualizowano} istniejących.'
                ))
            else:
                self.stdout.write(self.style.ERROR(f'Błąd połączenia: {response.status_code}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Wystąpił błąd: {e}'))