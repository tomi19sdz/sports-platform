import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Wyszukuje dane, ale nie panikuje, jeśli ich nie ma."""
    zapytanie = f"{mecz} football tactics stats tournament 2026"
    dane = ""
    try:
        with DDGS() as ddgs:
            wyniki = ddgs.news(zapytanie, region='wt-wt', max_results=5)
            for wynik in wyniki:
                dane += f"{wynik.get('title', '')}: {wynik.get('body', '')}\n"
    except Exception:
        pass # Jeśli wyszukiwarka nie działa, po prostu nie dodajemy danych z sieci
    return dane

def wygeneruj_analize_ai(mecz):
    """Generuje analizę ekspercką - zawsze pełną, nigdy niepustą."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: return "Błąd serwera."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    # SYSTEM PROMPT - Teraz wymuszamy kompleksowość
    system_prompt = """Jesteś elitarnym analitykiem sportowym. Twoim zadaniem jest stworzenie pełnej, profesjonalnej analizy meczowej.
ZASADA 1: Pierwsza linijka to ZAWSZE: '**Analiza oparta na informacjach źródłowych z: [DATA]**'.
ZASADA 2: Twoja analiza MUSI zawierać następujące sekcje:
   - Tło i kontekst historyczny (rywalizacja, znaczenie meczu).
   - Analiza stylu gry i taktyki obu drużyn.
   - Kluczowi zawodnicy i ich aktualny wpływ na grę.
   - Droga do finału / Podsumowanie turnieju (jeśli to mecz pucharowy).
   - Przewidywania i analiza scenariuszy.
   - '#### Przewidywany wynik' z konkretnym typem (np. 2:1).
ZASADA 3: Wykorzystaj dane z sieci, jeśli są dostępne. Jeśli dane z sieci są skąpe, użyj swojej eksperckiej wiedzy piłkarskiej, aby uzupełnić analizę. POD ŻADNYM POZOREM nie pisz, że nie masz danych."""

    user_prompt = f"Data: {dzisiejsza_data}. Analiza meczu: {mecz}. DANE Z SIECI: {swieze_dane}"

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.3
    )
    
    return odpowiedz.choices[0].message.content.strip()