import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Przeszukuje internet za darmo, aby znaleźć dzisiejsze newsy o meczu."""
    zapytanie = f"{mecz} zapowiedź meczu kontuzje aktualności"
    dzisiejsze_fakty = ""
    
    with DDGS() as ddgs:
        wyniki = ddgs.text(zapytanie, region='pl-pl', max_results=3)
        for wynik in wyniki:
            dzisiejsze_fakty += f"- Źródło: {wynik['title']}\nTreść: {wynik['body']}\n\n"
            
    return dzisiejsze_fakty

def wygeneruj_analize_ai(mecz):
    return "TEST - TO JEST TEN PLIK!"
    """Tworzy analizę: AI wnioskuje datę z artykułów, a Python wymusza jej wyświetlenie."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    
    if not ukryty_klucz:
        return "Błąd serwera: Nie znaleziono ukrytego klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    # SYSTEM PROMPT - Twarde zasady, których AI nie może złamać
    system_prompt = """Jesteś profesjonalnym analitykiem sportowym. 
ZASADA NR 1: W pierwszej linijce swojej odpowiedzi MUSISZ napisać TYLKO wywnioskowaną datę lub okres pochodzenia informacji (np. '15 lipca 2026' albo 'z ostatnich dni'). Nie pisz w pierwszej linijce niczego więcej!
ZASADA NR 2: Dopiero od drugiej linijki zacznij pisać właściwą analizę z nagłówkami."""

    # USER PROMPT - Konkretne zadanie
    user_prompt = f"""Dzisiejsza data: {dzisiejsza_data}.
Napisz analizę dla meczu: {mecz}. Opieraj się WYŁĄCZNIE na poniższych danych:

### ŚWIEŻE DANE Z INTERNETU: ###
{swieze_dane}
#################################

Pamiętaj o wymogach z ZASADY NR 1 i ZASADY NR 2!"""

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    surowy_tekst = odpowiedz.choices[0].message.content.strip()
    
    # Python rozdziela odpowiedź AI na pierwszą linijkę (datę) i resztę (analizę)
    podzial = surowy_tekst.split('\n', 1)
    
    wywnioskowana_data = podzial[0].strip().replace('**', '') # Czyścimy datę
    reszta_analizy = podzial[1].strip() if len(podzial) > 1 else ""
    
    # Składamy wszystko w nierozerwalną całość z wymuszonym pogrubieniem
    ostateczny_tekst = f"**Analiza oparta na informacjach źródłowych z: {wywnioskowana_data}**\n\n{reszta_analizy}"
    
    return ostateczny_tekst