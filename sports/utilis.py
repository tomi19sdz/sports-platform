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
    """Generuje bezbłędną i merytoryczną analizę opartą na świeżych faktach z sieci lub bazie wiedzy."""
    
    # Bezpieczne pobieranie klucza OpenAI ze zmiennych środowiskowych (.env)
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: 
        return "Błąd konfiguracji serwera: Brak klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    
    if swieze_dane:
        kontekst = f"DANE Z SIECI (najnowsze informacje o kontuzjach/formie):\n{swieze_dane}\n\nWpleć te konkretne informacje w swoją analizę i opisz aktualną formę."
    else:
        kontekst = "BRAK DANYCH Z INTERNETU. Użyj swojej obszernej wiedzy na temat historii, stylu gry, trenerów i standardowej taktyki tych drużyn, aby napisać rzetelną zapowiedź."

    # Rygorystyczny system prompt wymuszający poprawność merytoryczną i przypisanie graczy
    system_prompt = """Jesteś profesjonalnym, charyzmatycznym ekspertem piłkarskim, który pisze artykuły na portal sportowy.
ZASADY:
1. Nigdy nie odmawiaj napisania analizy. 
2. Jeśli w dostarczonych DANYCH Z SIECI są informacje o kontuzjach lub aktualnej formie - zrób z nich główny punkt analizy.
3. KRYTYCZNE: Bądź w 100% poprawny merytorycznie. Zanim przypiszesz piłkarza wymienionego w danych (np. Nico Williams, Lionel Messi) do konkretnej drużyny, upewnij się, w której reprezentacji lub klubie on RZECZYWIŚCIE gra. Kategorycznie zabrania się przypisywania gracza jednej drużyny do zespołu rywali!
4. Zakończ analizę sekcją '#### Przewidywany przebieg spotkania' z Twoim typem na wynik meczu."""

    user_prompt = f"Mecz do analizy: {mecz}\n\n{kontekst}"

    try:
        odpowiedz = klient.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1  # Niska temperatura drastycznie ogranicza zmyślanie i mieszanie faktów przez model
        )
        return odpowiedz.choices[0].message.content.strip()
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