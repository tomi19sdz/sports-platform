import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Próbuje pobrać dane z DDG. W razie blokady serwera zwraca None zamiast ubijać analizę."""
    # Prostsze zapytanie daje lepsze rezultaty w DDG
    zapytanie = f"{mecz} zapowiedź meczu OR kontuzje OR form"
    try:
        # Zmniejszamy timeout do 10, by strona nie ładowała się w nieskończoność przy blokadzie
        with DDGS(timeout=10) as ddgs:
            wyniki = [r for r in ddgs.text(zapytanie, max_results=3)]
        
        if not wyniki:
            return None
            
        return "\n".join([f"- {r.get('body', '')}" for r in wyniki])
    except Exception as e:
        # Print w konsoli pomoże Ci sprawdzić, czy PythonAnywhere blokuje ruch
        print(f"Blokada DDG lub błąd sieci: {e}")
        return None

def wygeneruj_analize_ai(mecz):
    """Generuje niesamowitą analizę, elastycznie dostosowując się do dostępnych danych."""
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: 
        return "Błąd konfiguracji serwera: Brak klucza OpenAI."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    
    # ELASTYCZNY KONTEKST:
    if swieze_dane:
        kontekst = f"DANE Z SIECI (najnowsze informacje o kontuzjach/formie):\n{swieze_dane}\n\nWpleć te informacje w swoją analizę i opisz aktualną formę."
    else:
        kontekst = "BRAK DANYCH Z INTERNETU. Użyj swojej obszernej wiedzy na temat historii, stylu gry, trenerów i standardowej taktyki tych drużyn, aby napisać rzetelną i wciągającą zapowiedź."

    # NOWY, WYZWOLONY PROMPT DLA AI
    system_prompt = """Jesteś profesjonalnym ekspertem piłkarskim, który pisze świetne artykuły na portal sportowy.
ZASADY:
1. Nigdy nie odmawiaj napisania analizy. 
2. Jeśli w dostarczonych DANYCH Z SIECI są informacje o konkretnych kontuzjach, osłabieniach lub aktualnej formie - koniecznie zrób z nich główny punkt analizy!
3. Jeśli brak danych w sieci, skup się na historii, mocnych i słabych stronach oraz stylu gry.
4. Zakończ analizę sekcją '#### Przewidywany przebieg spotkania' z Twoim typem na mecz.
5. KRYTYCZNE: Bądź w 100% poprawny merytorycznie. Jeśli wymieniasz piłkarza (np. na liście kontuzji), upewnij się, do jakiej drużyny należy! Nie przypisuj graczy z jednej reprezentacji/klubu do drugiej."""
    user_prompt = f"Mecz do analizy: {mecz}\n\n{kontekst}"

    try:
        odpowiedz = klient.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.6  # Zwiększyliśmy temperaturę! AI będzie teraz bardziej kreatywne i naturalne, a nie sztywne.
        )
        return odpowiedz.choices[0].message.content.strip()
    except Exception as e:
        return f"Wystąpił błąd komunikacji z modelem AI: {e}"

def aktualizuj_analize(stara_analiza, mecz):
    """Dokleja nową treść tylko, jeśli AI poprawnie ją wygenerowało."""
    nowa_tresc = wygeneruj_analize_ai(mecz)
    
    if "Wystąpił błąd komunikacji z modelem AI" in nowa_tresc or "Błąd konfiguracji" in nowa_tresc:
        return stara_analiza
        
    data_aktualizacji = date.today().strftime("%d.%m.%Y %H:%M")
    
    # Jeśli stara analiza jest pusta, oddajemy od razu nową
    if not stara_analiza or stara_analiza.strip() == "":
        return nowa_tresc
        
    return f"{stara_analiza}\n\n--- AKTUALIZACJA ({data_aktualizacji}):\n{nowa_tresc}"