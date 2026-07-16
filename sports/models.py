import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import load_dotenv
from openai import OpenAI

# --- ŁADOWANIE KLUCZA ---
# Zadziała i na Twoim komputerze, i na serwerze PythonAnywhere
load_dotenv() 
load_dotenv('/home/tomi19sdz/sports-platform/.env') 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- TWOJE BAZOWE MODELE ---

class Match(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    home_logo = models.URLField(null=True, blank=True)
    away_logo = models.URLField(null=True, blank=True)
    match_date = models.DateTimeField()

    # Pola na wynik
    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='SCHEDULED')

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"


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
    # Uruchom tylko dla nowo utworzonych meczów, które nie mają jeszcze analizy
    if created and not instance.analyses.exists():
        try:
            prompt = f"""Jako ekspert sportowy napisz 10 zdań analizy przedmeczowej o spotkaniu {instance.home_team} kontra {instance.away_team}. 
            Uwzględnij ich aktualną formę, potencjalne kontuzje i statystyki z tego sezonu. Przewidywany wynik spotkania.
            Tekst ma być rzeczowy, ekspercki i podzielony na przejrzyste akapity."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Jesteś cenionym ekspertem piłkarskim. Unikaj banałów."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content.strip()
            Analysis.objects.create(match=instance, content=ai_content)
            
        except Exception as e:
            # Rejestruje błąd w konsoli serwera w razie problemów z API
            print(f"Błąd generatora AI: {e}")