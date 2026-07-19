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
    """Tworzy analizę i samodzielnie wnioskuje datę zebranych informacji źródłowych."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    
    if not ukryty_klucz:
        return "Błąd serwera: Nie znaleziono ukrytego klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    
    swieze_dane = pobierz_swieze_dane(mecz)
    
    # Przekazujemy AI dzisiejszą datę, aby miało orientację w czasie
    dzisiejsza_data = date.today().strftime("%d.%m.%Y")
    
    prompt = f"""
    Jesteś profesjonalnym analitykiem sportowym dla portalu sportsplatform.pl. Dzisiejsza data to {dzisiejsza_data}.
    Napisz profesjonalną analizę dla meczu: {mecz}.
    
    ZABRANIAM CI opierać się na swojej historycznej wiedzy.
    Masz oprzeć się WYŁĄCZNIE na tych najświeższych informacjach pobranych z internetu:
    
    ### ŚWIEŻE DANE Z INTERNETU: ###
    {swieze_dane}
    #################################
    
    Na podstawie tych informacji, wymień krótko mocne i słabe strony z ostatnich dni i zaproponuj ostateczny typ.
    
    WYMÓG FORMALNY:
    Na samej górze swojej odpowiedzi MUSISZ napisać pogrubioną czcionką, z jakich dni/dat pochodzą informacje umieszczone w artykułach. Przeanalizuj treść danych (np. jeśli mówią o kontuzji z 15 lipca lub meczu z zeszłej środy, wpisz tę datę). Jeśli artykuły nie precyzują konkretnych dat wydarzeń, napisz po prostu, że są to informacje zebrane w dniu {dzisiejsza_data}.
    
    Format, jakiego masz użyć na samym początku (zawsze podawaj jako pierwsza linijka):
    **Analiza oparta na informacjach źródłowych z: [TUTAJ WPISZ WYWNIOSKOWANĄ DATĘ / OKRES]**
    """

    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    
    return odpowiedz.choices[0].message.content