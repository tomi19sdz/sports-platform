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
    analyses = serializers.SerializerMethodField() 

    class Meta:
        model = Match
        # DODAŁEM 'prediction_status' na końcu listy poniżej:
        fields = ['id', 'home_team', 'away_team', 'league', 'match_date', 'home_logo', 'away_logo', 'videos', 'analyses', 'home_score', 'away_score', 'status', 'prediction_status']

    def get_analyses(self, obj):
        approved_analyses = obj.analyses.filter(is_approved=True)
        return AnalysisSerializer(approved_analyses, many=True).data