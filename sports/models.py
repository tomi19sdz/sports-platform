import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dotenv import load_dotenv
from openai import OpenAI

# 1. Ładujemy klucz z pliku .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- TWOJE MODELE ---

class Match(models.Model):
    home_team = models.CharField(max_length=200)
    away_team = models.CharField(max_length=200)
    home_logo = models.URLField(null=True, blank=True)
    away_logo = models.URLField(null=True, blank=True)
    match_date = models.DateTimeField()
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

# --- INTELIGENTNY ROBOT DO ANALIZ ---

@receiver(post_save, sender=Match)
def create_ai_analysis(sender, instance, created, **kwargs):
    # Generuj analizę tylko dla nowych meczów, które jeszcze jej nie mają
    if created and not instance.analyses.exists():
        try:
            prompt = f"""Jako profesjonalny analityk sportowy, napisz szczegółową zapowiedź meczu {instance.home_team} vs {instance.away_team}. 
            W analizie zawrzyj:
            1. Analizę taktyczną obu zespołów.
            2. Kluczowe braki kadrowe i kontuzje.
            3. Historię ostatnich bezpośrednich spotkań.
            4. Ogólne podsumowanie i przewidywany scenariusz meczu.
            Tekst ma być rzeczowy, ekspercki i podzielony na przejrzyste akapity."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Jesteś cenionym ekspertem piłkarskim. Unikaj banałów."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content.strip()
            Analysis.objects.create(match=instance, content=ai_content)
            
        except Exception as e:
            print(f"Błąd generatora AI: {e}")