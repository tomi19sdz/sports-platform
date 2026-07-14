from django.db import models

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

# Twoje przywrócone wideo
class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField()
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