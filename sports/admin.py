from django.contrib import admin
from .models import Match, Analysis, ChatMessage, Video
from .utils import aktualizuj_analize  # Upewnij się, że funkcja jest w utils.py

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'match_date')
    search_fields = ('home_team', 'away_team')

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('match', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    actions = ['approve_analyses', 'update_analysis_ai']

    @admin.action(description="Zatwierdź wybrane analizy")
    def approve_analyses(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Aktualizuj analizę AI (dopisz nowe dane)")
    def update_analysis_ai(self, request, queryset):
        for obj in queryset:
            # Używamy pola 'content' tak jak w Twoim modelu
            stara_tresc = obj.content 
            mecz_nazwa = f"{obj.match.home_team} vs {obj.match.away_team}"
            
            # Wywołujemy funkcję aktualizującą
            obj.content = aktualizuj_analize(stara_tresc, mecz_nazwa)
            obj.save()

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'match', 'text', 'created_at')
    list_filter = ('match', 'created_at')
    search_fields = ('author', 'text')

admin.site.register(Video)