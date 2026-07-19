import os
from datetime import date # <-- Dodaliśmy import daty
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
    """Tworzy analizę na podstawie świeżych danych z widoczną datą."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    
    if not ukryty_klucz:
        return "Błąd serwera: Nie znaleziono ukrytego klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    
    swieze_dane = pobierz_swieze_dane(mecz)
    
    # Pobieramy dzisiejszą datę w formacie DD.MM.YYYY
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    prompt = f"""
    Jesteś profesjonalnym analitykiem sportowym dla portalu sportsplatform.pl. 
    Napisz profesjonalną analizę dla meczu: {mecz}.
    
    ZABRANIAM CI opierać się na swojej historycznej wiedzy, ponieważ jest przestarzała.
    Masz oprzeć się WYŁĄCZNIE na tych najświeższych informacjach z dzisiaj, które pobrałem z internetu:
    
    ### ŚWIEŻE DANE Z INTERNETU: ###
    {swieze_dane}
    #################################
    
    Na podstawie tych informacji, wymień krótko mocne i słabe strony z ostatnich dni i zaproponuj ostateczny typ (np. Wygrana gospodarzy).
    
    WYMÓG FORMALNY: 
    Na samym początku swojej odpowiedzi MUSISZ umieścić pogrubioną linijkę o treści:
    **Analiza oparta na najświeższych danych z dnia: {dzisiejsza_data}**
    """

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return odpowiedz.choices[0].message.content