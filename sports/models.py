from django.db import models

class Match(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_logo = models.URLField(max_length=500, blank=True, null=True)
    away_logo = models.URLField(max_length=500, blank=True, null=True)
    match_date = models.DateTimeField()

class Video(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField()

class Analysis(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='analyses')
    content = models.TextField()
    
    # NOWE POLE: Domyślnie każda nowa analiza jest ukryta (False)
    is_approved = models.BooleanField(default=False) 
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analiza do meczu: {self.match.home_team} vs {self.match.away_team}"