import os
from datetime import date
from django.conf import settings
from openai import OpenAI
from tavily import TavilyClient

def pobierz_swieze_dane(mecz):
    """Pobiera prawdziwe dane z internetu za pomocą niezawodnego API Tavily."""
    
    # Bezpieczne pobieranie klucza Tavily ze zmiennych środowiskowych (.env)
    tavily_klucz = os.environ.get("TAVILY_API_KEY", getattr(settings, "TAVILY_API_KEY", None))
    
    if not tavily_klucz:
        print("BŁĄD: Brak klucza TAVILY_API_KEY w konfiguracji / pliku .env!")
        return None

    try:
        tavily = TavilyClient(api_key=tavily_klucz)
        # Dynamiczne zapytanie z uwzględnieniem bieżącego roku
        zapytanie = f"{mecz} zapowiedź meczu kontuzje składy {date.today().year}"
        
        # Pobieranie 3 najbardziej dopasowanych wyników z sieci
        odpowiedz = tavily.search(query=zapytanie, search_depth="basic", max_results=3)
        
        if not odpowiedz.get('results'):
            return None
            
        # Agregacja treści pobranych artykułów
        kontekst = "\n".join([f"- {wynik['content']}" for wynik in odpowiedz['results']])
        return kontekst
    except Exception as e:
        print(f"Błąd wyszukiwania Tavily: {e}")
        return None

def wygeneruj_analize_ai(mecz):
    """Generuje bezbłędną analizę przedmeczową, stosując wymuszone sprawdzanie faktów (Chain of Thought)."""
    
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: 
        return "Błąd konfiguracji serwera: Brak klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    
    if swieze_dane:
        kontekst = f"DANE Z SIECI:\n{swieze_dane}"
    else:
        kontekst = "Brak najnowszych doniesień. Oprzyj się na ogólnej wiedzy o stylu gry obu zespołów."

    # POTĘŻNY SYSTEM PROMPT Z WYMUSZONYM BLOKIEM MYŚLENIA
    system_prompt = """Jesteś elitarnym analitykiem sportowym. 
Każdą odpowiedź MUSISZ zacząć od sekcji weryfikacyjnej zamkniętej w znacznikach START_THINKING oraz END_THINKING. 
W tej sekcji wypisz wszystkich kluczowych piłkarzy wymienionych w danych z sieci i przypisz im PRAWIDŁOWĄ reprezentację/klub (np. Nico Williams = Hiszpania, Lionel Messi = Argentyna).

Przykład startu odpowiedzi:
START_THINKING
- Nico Williams: reprezentacja Hiszpanii (kontuzja hamstringu)
- Lionel Messi: reprezentacja Argentyny
END_THINKING

We właściwym artykule (który piszesz DOPIERO PO znaczniku END_THINKING) kategorycznie zabraniam Ci mylić drużyny zawodników. Jeśli ktoś jest z Hiszpanii, pisz o nim wyłącznie w sekcji o Hiszpanii!
Artykuł ma być charyzmatyczny, profesjonalny i kończyć się sekcją '#### Przewidywany przebieg spotkania' z Twoim typem na wynik meczu."""

    user_prompt = f"Mecz do analizy: {mecz}\n\n{kontekst}"

    try:
        odpowiedz = klient.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        pelny_tekst = odpowiedz.choices[0].message.content.strip()
        
        # --- SPRZĄTANIE KODEM (Magia Pythona) ---
        # Jeśli model wygenerował blok myślenia, odcinamy go, żeby ukryć go przed użytkownikiem
        if "END_THINKING" in pelny_tekst:
            czysta_analiza = pelny_tekst.split("END_THINKING")[-1].strip()
            return czysta_analiza
            
        return pelny_tekst
    except Exception as e:
        return f"Wystąpił błąd komunikacji z modelem AI: {e}"

def aktualizuj_analize(stara_analiza, mecz):
    """Dokleja nową treść tylko, jeśli AI poprawnie ją wygenerowało."""
    nowa_tresc = wygeneruj_analize_ai(mecz)
    
    if "Wystąpił błąd komunikacji" in nowa_tresc or "Błąd konfiguracji" in nowa_tresc:
        return stara_analiza
        
    data_aktualizacji = date.today().strftime("%d.%m.%Y %H:%M")
    
    if not stara_analiza or stara_analiza.strip() == "":
        return nowa_tresc
        
    return f"{stara_analiza}\n\n--- AKTUALIZACJA ({data_aktualizacji}):\n{nowa_tresc}"