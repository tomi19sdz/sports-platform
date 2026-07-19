import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Wyszukuje dane z naciskiem na drogę turniejową i formę w trakcie zawodów."""
    # Dodajemy słowa kluczowe 'road to final' i 'tournament stats', żeby wymusić konkrety
    zapytanie = f"{mecz} football match tournament road to final stats performance 2026"
    dane = ""
    try:
        with DDGS() as ddgs:
            # Pobieramy 6 newsów z globalnych źródeł
            wyniki = ddgs.news(zapytanie, region='wt-wt', max_results=6)
            for wynik in wyniki:
                dane += f"{wynik.get('title', '')}: {wynik.get('body', '')}\n"
    except Exception:
        return "Brak danych z sieci."
    return dane

def wygeneruj_analize_ai(mecz):
    """Generuje analizę z rygorystycznym wymogiem opisu turnieju."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: return "Błąd serwera."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    # SYSTEM PROMPT - Dodajemy instrukcję o "drodze do finału"
    system_prompt = """Jesteś elitarnym analitykiem sportowym. 
ZASADA 1: Pierwsza linijka to ZAWSZE: '**Analiza oparta na informacjach źródłowych z: [DATA]**'.
ZASADA 2: Jeśli mecz jest częścią turnieju (np. Mistrzostwa Świata, Euro), MUSISZ opisać drogę obu drużyn do tego meczu (tzw. 'road to final'). Wymień, jak sobie radziły w fazie grupowej i pucharowej.
ZASADA 3: Jeśli w danych są konkretne nazwiska (np. Lamine Yamal), MUSISZ je wymienić w kontekście ich formy w tym turnieju. Nie zmyślaj nazwisk, jeśli nie ma ich w danych - opisuj wtedy pozycje (np. 'skrzydłowy').
ZASADA 4: Na końcu MUSISZ podać nagłówek '#### Przewidywany wynik' i konkretny typ (np. 2:1)."""

    user_prompt = f"Data: {dzisiejsza_data}. Analiza meczu: {mecz}. DANE Z SIECI (drogę do finału/turniej): {swieze_dane}"

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.2 
    )
    
    return odpowiedz.choices[0].message.content.strip()