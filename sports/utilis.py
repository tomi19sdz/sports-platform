import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Przeszukuje dzisiejsze WIADOMOŚCI (news), aby znaleźć najświeższe konkrety."""
    zapytanie = f"{mecz} piłka nożna finał zapowiedź składy kontuzje"
    dzisiejsze_fakty = ""
    
    with DDGS() as ddgs:
        # Przeszukujemy zakładkę News (wiadomości) dla większej dawki konkretów
        wyniki = ddgs.news(zapytanie, region='pl-pl', max_results=6)
        for wynik in wyniki:
            tytul = wynik.get('title', 'Brak tytułu')
            tresc = wynik.get('body', 'Brak treści')
            dzisiejsze_fakty += f"- Nagłówek: {tytul}\nTreść: {tresc}\n\n"
            
    return dzisiejsze_fakty

def wygeneruj_analize_ai(mecz):
    """Tworzy analizę i wymusza podanie konkretnego wyniku."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    
    if not ukryty_klucz:
        return "Błąd serwera: Nie znaleziono ukrytego klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    
    swieze_dane = pobierz_swieze_dane(mecz)
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    # SYSTEM PROMPT - Zaostrzone zasady z wymuszonym wynikiem
    system_prompt = """Jesteś profesjonalnym analitykiem sportowym. 
ZASADA NR 1: W pierwszej linijce swojej odpowiedzi MUSISZ napisać TYLKO wywnioskowaną datę lub okres pochodzenia informacji. Nie pisz w pierwszej linijce niczego więcej!
ZASADA NR 2: Od drugiej linijki zacznij pisać właściwą analizę z nagłówkami.
ZASADA NR 3: Na samym końcu analizy MUSISZ utworzyć nagłówek '#### Przewidywany wynik' i podać tam konkretny typ liczbowy (np. 2:1, 0:0, 3:0), nawet jeśli brakuje Ci danych w artykułach i musisz zgadywać na podstawie ogólnego potencjału drużyn!"""

    user_prompt = f"""Dzisiejsza data: {dzisiejsza_data}.
Napisz analizę dla meczu: {mecz}. Opieraj się WYŁĄCZNIE na poniższych danych, ale zachowaj ZASADĘ NR 3.

### ŚWIEŻE DANE Z INTERNETU: ###
{swieze_dane}
#################################
"""

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    
    surowy_tekst = odpowiedz.choices[0].message.content.strip()
    
    podzial = surowy_tekst.split('\n', 1)
    
    wywnioskowana_data = podzial[0].strip().replace('**', '') 
    reszta_analizy = podzial[1].strip() if len(podzial) > 1 else ""
    
    ostateczny_tekst = f"**Analiza oparta na informacjach źródłowych z: {wywnioskowana_data}**\n\n{reszta_analizy}"
    
    return ostateczny_tekst