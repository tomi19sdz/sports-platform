import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Przeszukuje cały światowy internet w poszukiwaniu konkretów."""
    # Zmieniamy zapytanie na angielskie, żeby wyciągnąć profesjonalne analizy
    zapytanie = f"{mecz} football match analysis, tactics, starting lineups, injuries, expert preview"
    dane = ""
    
    with DDGS() as ddgs:
        # Region 'wt-wt' (Worldwide) przeszukuje globalne portale sportowe
        wyniki_news = ddgs.news(zapytanie, region='wt-wt', max_results=8)
        wyniki_text = ddgs.text(zapytanie, region='wt-wt', max_results=5)
        
        for wynik in list(wyniki_news) + list(wyniki_text):
            tytul = wynik.get('title', '')
            tresc = wynik.get('body', '')
            dane += f"- {tytul}: {tresc}\n"
            
    return dane

def wygeneruj_analize_ai(mecz):
    """Tworzy analizę ekspercką na bazie globalnych danych."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: return "Błąd serwera."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    system_prompt = """Jesteś elitarnym analitykiem sportowym. 
ZASADA 1: Pierwsza linijka to ZAWSZE: '**Analiza oparta na informacjach źródłowych z: [DATA]**'.
ZASADA 2: Jesteś ekspertem. W swojej analizie MUSISZ:
   - Wymienić przewidywane składy (jeśli dane na to pozwalają).
   - Przeanalizować taktykę (ustawienie, pressing, kluczowe strefy boiska).
   - Wskazać kluczowe pojedynki indywidualne (np. napastnik vs obrońca).
   - Nie używaj ogólników o 'bogatej historii'. Skup się na formacie meczu, który analizujesz (np. finał).
ZASADA 3: Na końcu MUSISZ podać nagłówek '#### Przewidywany wynik' i konkretny typ (np. 2:1)."""

    user_prompt = f"""Dzisiejsza data: {dzisiejsza_data}.
Napisz głęboką analizę techniczną dla meczu: {mecz}.
Wykorzystaj te globalne dane z internetu:
{swieze_dane}
"""

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.3 # Obniżamy temperaturę, żeby AI było bardziej "konkretne", a mniej "kreatywne"
    )
    
    return odpowiedz.choices[0].message.content.strip()