from django.contrib import admin
from django import forms
from django.forms import widgets
from django.utils.safestring import mark_safe
from .models import Match, Analysis, ChatMessage

# 1. Tworzymy specjalny widget (hybrydę pola tekstowego i listy)
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


# 2. Tworzymy niestandardowy formularz dla panelu admina
class MatchAdminForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pobieramy wszystkie unikalne nazwy lig, które JUŻ SĄ w bazie (i nie są puste)
        leagues = Match.objects.exclude(league__isnull=True).exclude(league__exact='').values_list('league', flat=True).distinct()
        
        # Podpinamy nasz widget do pola 'league'
        if 'league' in self.fields:
            self.fields['league'].widget = DatalistWidget(data_list=leagues, name='league')
            self.fields['league'].help_text = "Wybierz z listy lub wpisz zupełnie nową ligę."


# 3. Rejestrujemy model Match z nowym formularzem
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    form = MatchAdminForm
    
    # Opcjonalnie: ułatwia przeglądanie meczów w tabeli w panelu admina
    list_display = ('home_team', 'away_team', 'league', 'match_date', 'status')
    list_filter = ('league', 'status')
    search_fields = ('home_team', 'away_team', 'league')

# Jeśli masz już zarejestrowane inne modele, zostaw je poniżej, np:
# admin.site.register(Analysis)
# admin.site.register(ChatMessage)