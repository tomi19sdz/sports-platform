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
        # Dynamiczne zapytanie wymuszające szukanie formy, kontuzji i kursów
        zapytanie = f"{mecz} zapowiedź meczu ostatnie wyniki kontuzje składy kursy bukmacherskie {date.today().year}"
        
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
        kontekst = f"DANE Z SIECI (Ostatnia forma, kursy, kontuzje):\n{swieze_dane}"
    else:
        kontekst = "Brak najnowszych doniesień. Oprzyj się na ogólnej wiedzy o aktualnym sezonie obu zespołów."

    # POTĘŻNY SYSTEM PROMPT: ŁĄCZY TWOJE ZABEZPIECZENIA KADROWE Z MOJĄ LOGIKĄ BUKMACHERSKĄ
    system_prompt = """Jesteś elitarnym analitykiem sportowym i ekspertem od wykrywania niespodzianek bukmacherskich. 
Każdą odpowiedź MUSISZ zacząć od sekcji weryfikacyjnej zamkniętej w znacznikach START_THINKING oraz END_THINKING. 
W tej sekcji wykonaj następujące kroki:
1. Wypisz wszystkich kluczowych piłkarzy wymienionych w danych z sieci i przypisz im PRAWIDŁOWĄ reprezentację/klub (np. Nico Williams = Hiszpania, Lionel Messi = Argentyna).
2. Zidentyfikuj realną formę obu drużyn (czy faworyt ostatnio wygrywa łatwo, czy się męczy).
3. Wypisz kluczowe absencje/kontuzje mające wpływ na mecz.
4. Oceń, czy kursy/status faworyta są adekwatne do rzeczywistości, czy to pułapka.

Przykład startu odpowiedzi:
START_THINKING
- Nico Williams: reprezentacja Hiszpanii (kontuzja hamstringu)
- Lionel Messi: reprezentacja Argentyny
- Forma: Gospodarze wygrali 1 z ostatnich 5 meczów. Goście regularnie punktują.
- Wniosek: Faworyt jest w kryzysie, to pułapka. Unikam typowania wysokiego wyniku dla gospodarzy.
END_THINKING

We właściwej analizie (która zaczyna się DOPIERO PO znaczniku END_THINKING) przestrzegaj tych BEZWZGLĘDNYCH ZASAD:
1. Kategorycznie zabraniam Ci mylić drużyny zawodników. Jeśli ktoś jest z Hiszpanii, pisz o nim wyłącznie w sekcji o Hiszpanii!
2. Odrzuć mit marki: Jeśli faworyt męczy się w ostatnich meczach lub ma braki kadrowe, ZAKAZUJĘ Ci typowania jego gładkiego zwycięstwa (np. 3:0).
3. Koniec z leniwym wynikiem 1:1 i 2:1: Jeśli jedna z drużyn wyraźnie dominuje i jest zdrowa, typuj odważnie wysoki wynik odzwierciedlający kurs. Remisy rezerwuj WYŁĄCZNIE dla wyrównanych zespołów.
4. Artykuł ma być charyzmatyczny, profesjonalny i kończyć się sekcją '#### Przewidywany przebieg spotkania' z Twoim typem.

Na samym końcu analizy wygeneruj podsumowanie w DOKŁADNIE takiej formie:
#### Przewidywany przebieg spotkania
- **Proponowany typ:** (np. Wygrana gospodarzy / Under 2.5 bramki)
- **Proponowany dokładny wynik:** (Konkretny wynik oparty o weryfikację formy, np. 0:2)"""

    user_prompt = f"Mecz do analizy: {mecz}\n\n{kontekst}"

    try:
        odpowiedz = klient.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1 # Bardzo niska temperatura dla maksymalnej precyzji faktów
        )
        
        pelny_tekst = odpowiedz.choices[0].message.content.strip()
        
        # --- SPRZĄTANIE KODEM ---
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