import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Bezpieczne wyszukiwanie z obsługą błędów."""
    zapytanie = f"{mecz} football match analysis, tactics, starting lineups"
    dane = ""
    
    try:
        with DDGS() as ddgs:
            # Próbujemy pobrać dane
            wyniki_news = ddgs.news(zapytanie, region='wt-wt', max_results=3)
            for wynik in wyniki_news:
                dane += f"- {wynik.get('title', '')}: {wynik.get('body', '')}\n"
    except Exception as e:
        # Jeśli wystąpi błąd (np. 403), zwracamy informację, że sieć jest niedostępna
        return "Błąd wyszukiwania (DuckDuckGo zablokowało dostęp). Używam ogólnej wiedzy."
            
    return dane

def wygeneruj_analize_ai(mecz):
    """Generuje analizę z 'bezpiecznikiem'."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: return "Błąd serwera."

    klient = OpenAI(api_key=ukryty_klucz)
    
    # Pobieramy dane (zabezpieczone przed błędem 403)
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    system_prompt = """Jesteś elitarnym analitykiem sportowym. 
Jeśli w danych wejściowych widzisz 'Błąd wyszukiwania', napisz profesjonalną analizę opartą na swoim doświadczeniu, zachowując styl ekspercki.
ZASADA 1: Pierwsza linijka to ZAWSZE: '**Analiza oparta na informacjach źródłowych z: [DATA]**'.
ZASADA 2: Na końcu MUSISZ podać nagłówek '#### Przewidywany wynik' i konkretny typ (np. 2:1)."""

    user_prompt = f"Dzisiejsza data: {dzisiejsza_data}. Analiza dla: {mecz}. DANE: {swieze_dane}"

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.3
    )
    
    return odpowiedz.choices[0].message.content.strip()