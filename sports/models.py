import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import load_dotenv
from .utils import wygeneruj_analize_ai

# --- ŁADOWANIE KLUCZA ---
load_dotenv()
load_dotenv('/home/tomi19sdz/sports-platform/.env')

# --- TWOJE BAZOWE MODELE ---

class Match(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    league = models.CharField(max_length=200, default="Inna") # NOWA KOLUMNA
    home_logo = models.URLField(null=True, blank=True)
    away_logo = models.URLField(null=True, blank=True)
    match_date = models.DateTimeField()
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='SCHEDULED')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.league})"

class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    video_url = models.URLField()
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "Wideo"

class Analysis(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='analyses')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

class ChatMessage(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# --- INTELIGENTNY ROBOT DO ANALIZ (Sygnał post_save) ---

@receiver(post_save, sender=Match)
def create_ai_analysis(sender, instance, created, **kwargs):
    if created and not instance.analyses.exists():
        try:
            # 1. Budujemy nazwę meczu z uwzględnieniem ligi
            nazwa_meczu = f"{instance.home_team} vs {instance.away_team} w lidze {instance.league}"
            
            # 2. Uruchamiamy generator AI
            gotowy_tekst = wygeneruj_analize_ai(nazwa_meczu)
            
            # 3. Zapisujemy wynik
            Analysis.objects.create(
                match=instance, 
                content=gotowy_tekst
            )
        except Exception as e:
            print(f"Błąd podczas automatycznego generowania analizy: {e}")