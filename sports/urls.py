import os
from datetime import date
from django.conf import settings
from duckduckgo_search import DDGS
from openai import OpenAI

def pobierz_swieze_dane(mecz):
    zapytanie = f"{mecz} football match stats 2026"
    try:
        with DDGS() as ddgs:
            wyniki = [r for r in ddgs.text(zapytanie, max_results=3)]
        if not wyniki: return "BRAK_DANYCH"
        return "\n".join([f"{r.get('title', '')}: {r.get('body', '')}" for r in wyniki])
    except Exception:
        return "BŁĄD_SIECI"

def wygeneruj_analize_ai(mecz):
    ukryty_klucz = os.environ.get("OPENAI_API_KEY", getattr(settings, "OPENAI_API_KEY", None))
    if not ukryty_klucz: return "Błąd serwera."
    klient = OpenAI(api_key=ukryty_klucz)
    swieze_dane = pobierz_swieze_dane(mecz)
    if swieze_dane == "BŁĄD_SIECI": return "Aktualnie nie możemy połączyć się ze źródłami."
    if swieze_dane == "BRAK_DANYCH": return "Analiza w przygotowaniu. Rzetelne zestawienie pojawi się przed meczem."

    system_prompt = "Jesteś profesjonalnym analitykiem sportowym. Analizuj WYŁĄCZNIE na podstawie danych. Podsumuj w '#### Przewidywany wynik'."
    odpowiedz = klient.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": f"Analiza: {mecz}. DANE: {swieze_dane}"}],
        temperature=0.1
    )
    return odpowiedz.choices[0].message.content.strip()

def aktualizuj_analize(stara_analiza, mecz):
    nowa_tresc = wygeneruj_analize_ai(mecz)
    if "Aktualnie nie możemy" in nowa_tresc or "Analiza w przygotowaniu" in nowa_tresc:
        return stara_analiza
    data = date.today().strftime("%d.%m.%Y %H:%M")
    return f"{stara_analiza}\n\n--- AKTUALIZACJA ({data}):\n{nowa_tresc}"