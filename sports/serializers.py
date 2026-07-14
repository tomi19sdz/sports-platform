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
    # 1. ZMIENIONA LINIJKA:
    analyses = serializers.SerializerMethodField() 

    class Meta:
        model = Match
        # TUTAJ DODANE NOWE POLA NA KOŃCU LISTY:
        fields = ['id', 'home_team', 'away_team', 'match_date', 'home_logo', 'away_logo', 'videos', 'analyses', 'home_score', 'away_score', 'status']

    # 2. NOWA FUNKCJA NA SAMYM DOLE (pamiętaj o wcięciach!):
    def get_analyses(self, obj):
        # Pobieramy tylko te, które mają zaznaczone is_approved
        approved_analyses = obj.analyses.filter(is_approved=True)
        return AnalysisSerializer(approved_analyses, many=True).data