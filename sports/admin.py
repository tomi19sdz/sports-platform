from django.contrib import admin
from .models import Match, Analysis, ChatMessage, Video

# Rejestracja wideo
admin.site.register(Video)

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date')
    search_fields = ('home_team', 'away_team')

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('match', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_analyses']

    def approve_analyses(self, request, queryset):
        queryset.update(is_approved=True)
    approve_analyses.short_description = "Zatwierdź wybrane analizy"

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'match', 'text', 'created_at')
    list_filter = ('match', 'created_at')
    search_fields = ('author', 'text')