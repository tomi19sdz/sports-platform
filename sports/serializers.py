from rest_framework import serializers
from .models import Match, Video, Analysis

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'video_url']

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['id', 'content']

class MatchSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    analyses = AnalysisSerializer(many=True, read_only=True) # <-- NOWE POŁĄCZENIE

    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'match_date', 'home_logo', 'away_logo', 'videos', 'analyses']