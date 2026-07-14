from django.contrib import admin
from .models import Match, Analysis, ChatMessage

# Rozbudowany widok dla Meczów
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date')
    search_fields = ('home_team', 'away_team')

# Rozbudowany widok dla Analiz (z opcją szybkiego zatwierdzania)
@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('match', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_analyses']

    def approve_analyses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_analyses.short_description = "Zatwierdź wybrane analizy"

# Rozbudowany widok dla Czatu (żeby łatwo usuwać spam)
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'match', 'text', 'created_at')
    list_filter = ('match', 'created_at')
    search_fields = ('author', 'text')