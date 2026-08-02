from django.contrib import admin
from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import Match, Analysis, ChatMessage, Video
from .utils import aktualizuj_analize

# ==========================================
# 1. WIDGET DATALIST (Hybryda pola i listy)
# ==========================================
class DatalistWidget(widgets.TextInput):
    def __init__(self, data_list, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name
        self._list = data_list
        # Dodajemy atrybut 'list' do pola <input>
        self.attrs.update({'list': f'list__{self._name}'})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super().render(name, value, attrs=attrs, renderer=renderer)
        # Budujemy ukrytą listę podpowiedzi <datalist>
        data_html = f'<datalist id="list__{self._name}">'
        for item in self._list:
            data_html += f'<option value="{item}">'
        data_html += '</datalist>'
        return mark_safe(text_html + data_html)

# ==========================================
# 2. FORMULARZ DLA MECZÓW
# ==========================================
class MatchAdminForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'
        widgets = {
            'status': forms.Select(choices=[
                ('SHEDULED', 'Zaplanowany (SCHEDULED)'),
                ('IN_PLAY', 'W trakcie (IN_PLAY)'),
                ('PAUSED', 'Przerwa (PAUSED)'),
                ('FINISHED', 'Zakończony (FINISHED)'),
            
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pobieramy wszystkie unikalne nazwy lig, które już są w bazie
        leagues = Match.objects.exclude(league__isnull=True).exclude(league__exact='').values_list('league', flat=True).distinct()
        
        # Podpinamy nasz widget do pola 'league'
        if 'league' in self.fields:
            self.fields['league'].widget = DatalistWidget(data_list=leagues, name='league')
            self.fields['league'].help_text = "Wybierz z listy lub wpisz zupełnie nową ligę."


# ==========================================
# 3. ZAREJESTROWANE MODELE ADMINA
# ==========================================
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    form = MatchAdminForm # <--- Podpięcie nowego formularza z podpowiedziami lig
    
    list_display = ('home_team', 'away_team', 'league', 'match_date', 'prediction_status')
    list_editable = ('prediction_status',) # Pozwala zmieniać status bezpośrednio na liście
    search_fields = ('home_team', 'away_team', 'league')
    fields = ('home_team', 'away_team', 'league', 'home_logo', 'away_logo', 'match_date', 'home_score', 'away_score', 'status', 'prediction_status')

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
            stara_tresc = obj.content 
            mecz_nazwa = f"{obj.match.home_team} vs {obj.match.away_team} w {obj.match.league}"
            obj.content = aktualizuj_analize(stara_tresc, mecz_nazwa)
            obj.save()

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'match', 'text', 'created_at')
    list_filter = ('match', 'created_at')
    search_fields = ('author', 'text')

admin.site.register(Video)