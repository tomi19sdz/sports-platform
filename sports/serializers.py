from rest_framework import serializers
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        # '__all__' sprawi, że API wyśle absolutnie wszystkie dane, łącznie z herbami
        fields = '__all__'