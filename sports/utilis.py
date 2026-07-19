import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    """Szuka faktów przy użyciu bardziej stabilnej metody text()."""
    zapytanie = f"{mecz} match preview stats injuries lineup 2026"
    try:
        with DDGS(timeout=30) as ddgs:
            # Używamy metody text(), która jest stabilniejsza na serwerach
            wyniki = [r for r in ddgs.text(zapytanie, max_results=3)]
        
        if not wyniki:
            return "BRAK_DANYCH"
            
        return "\n".join([f"{r.get('title', '')}: {r.get('body', '')}" for r in wyniki])
    except Exception:
        return "BŁĄD_SIECI"

def wygeneruj_analize_ai(mecz):
    """Generuje profesjonalną analizę lub informuje o oczekiwaniu na dane."""
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: 
        return "Błąd konfiguracji serwera."

    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    
    if swieze_dane == "BŁĄD_SIECI":
        return "Nasz dział analiz pracuje nad tą analizą. Zapraszamy 1-4 godziny przed meczem"
    
    if swieze_dane == "BRAK_DANYCH":
        return "Analiza jest w przygotowaniu. Nasz dział analiz przygotuje rzetelne zestawienie 1-4 godziny przed rozpoczęciem spotkania, gdy tylko pojawią się oficjalne składy i raporty meczowe."

    system_prompt = """Jesteś profesjonalnym analitykiem sportowym przygotowującym raport dla graczy.
ZASADA: Analiza musi opierać się WYŁĄCZNIE na dostarczonych danych z sieci.
1. Jeśli dane wspominają o kontuzjach – wymień je.
2. Jeśli dane mówią o taktyce – opisz ją.
3. Jeśli danych o jakimś aspekcie (np. kontuzje) nie ma – pomiń ten punkt, nie zmyślaj.
4. Podsumuj dane w sekcji '#### Przewidywany wynik', uzasadniając typ statystykami z dostarczonych źródeł."""

    user_prompt = f"Analiza dla: {mecz}. DANE Z SIECI: {swieze_dane}"

    try:
        odpowiedz = klient.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            temperature=0.1
        )
        return odpowiedz.choices[0].message.content.strip()
    except Exception:
        return "Wystąpił błąd podczas generowania analizy przez system AI."

def aktualizuj_analize(stara_analiza, mecz):
    """Dokleja tylko rzetelne, nowe analizy. W przypadku błędów zostawia wszystko bez zmian."""
    nowa_tresc = wygeneruj_analize_ai(mecz)
    
    # Warunki, w których nie dopisujemy błędu do analizy
    if "Nasz dział analiz pracuje" in nowa_tresc or "Analiza jest w przygotowaniu" in nowa_tresc or "Wystąpił błąd" in nowa_tresc:
        return stara_analiza
        
    data_aktualizacji = date.today().strftime("%d.%m.%Y %H:%M")
    
    # Łączymy stare z nowym tylko wtedy, gdy nowa treść jest wartościowa
    return f"{stara_analiza}\n\n--- AKTUALIZACJA ({data_aktualizacji}):\n{nowa_tresc}"