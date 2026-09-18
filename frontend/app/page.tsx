import Link from 'next/link';
import React from 'react';

// 1. Dodany interfejs dla analiz
interface Analysis {
  id: number;
  content: string;
}

interface Match {
  id: number;
  home_team: string;
  away_team: string;
  league: string;
  home_logo: string | null;
  away_logo: string | null;
  match_date: string;
  home_score: number | null;
  away_score: number | null;
  status: string;
  is_valuebet?: boolean;
  analyses?: Analysis[]; // 2. Dodane pole analyses
}

async function getMatches() {
  const res = await fetch('https://tomi19sdz.pythonanywhere.com/api/matches/', {
    next: { revalidate: 60 } 
  });
  if (!res.ok) return {};
  return res.json() as Promise<Record<string, Match[]>>;
}

export default async function HomePage() {
  const groupedMatches = await getMatches();
  
  const todayStr = new Date().toISOString().split('T')[0];
  const upcomingMatches = Object.entries(groupedMatches).filter(([date]) => date >= todayStr);

  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center mt-10">
          <h1 className="text-5xl font-black text-white mb-6 tracking-tight">
            Sports <span className="text-emerald-500">Platform</span>
          </h1>
          
          <div className="max-w-3xl mx-auto mb-10 text-center">
            <p className="text-slate-400 leading-relaxed text-lg">
              Witaj na <strong className="text-emerald-400 font-semibold">Sports Platform</strong> – Twoim niezawodnym źródle zaawansowanych statystyk sportowych i przedmeczowych analiz. 
              Nasz autorski system oparty na sztucznej inteligencji na bieżąco monitoruje kontuzje, realną formę zespołów oraz rynkowe kursy, dostarczając Ci najbardziej prawdopodobne typy i dokładne wyniki. Śledź na żywo zmagania najlepszych lig i podejmuj świadome decyzje na podstawie twardych danych.
            </p>
          </div>
        </header>

        {upcomingMatches.length === 0 ? (
          <div className="text-center text-slate-500 mt-20 flex flex-col items-center">
            <span className="text-6xl mb-4">🏟️</span>
            <p className="text-xl">Brak nadchodzących meczów.</p>
          </div>
        ) : (
          upcomingMatches.map(([date, matches]) => (
            <div key={date} className="mb-12">
              <h2 className="text-2xl font-bold text-emerald-400 mb-6 border-b border-slate-800/80 pb-3 flex items-center">
                <span className="bg-emerald-500/10 text-emerald-500 px-3 py-1 rounded-lg text-sm mr-3 border border-emerald-500/20">📅</span>
                {date}
              </h2>
              
              <div className="grid gap-4">
                {matches.map((match) => {
                  const isHot = match.is_valuebet;
                  
                  const cardTheme = isHot 
                    ? "bg-red-950/10 border-red-900/60 hover:border-red-500 hover:bg-red-900/30 shadow-[0_0_15px_rgba(239,68,68,0.15)]" 
                    : "bg-slate-900/40 border-slate-800/80 hover:border-emerald-500/50 hover:bg-slate-800/60 shadow-black/20";
                    
                  const scoreTheme = isHot
                    ? "bg-red-500/10 text-red-400 border-red-500/30 group-hover:border-red-500/60"
                    : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 group-hover:border-emerald-500/60";
                    
                  const vsTheme = isHot
                    ? "bg-red-950/50 text-red-400 border-red-800/50 group-hover:text-red-500 group-hover:border-red-500/80"
                    : "bg-slate-950 text-slate-400 border-slate-700/50 group-hover:text-emerald-500 group-hover:border-emerald-500/50";

                  // 3. Wyciąganie tekstu analizy (z odcięciem bloku technicznego)
                  const previewText = match.analyses && match.analyses.length > 0 
                    ? match.analyses[0].content.split('[DANE_SYSTEMU]')[0] 
                    : null;

                  return (
                    <Link key={match.id} href={`/match/${match.id}`} className={`relative rounded-2xl p-6 hover:-translate-y-1 transition-all duration-300 flex flex-col group shadow-lg border ${cardTheme}`}>
                      
                      {/* --- KONTENER GÓRNY (DRUŻYNY I WYNIK) --- */}
                      <div className="flex flex-col sm:flex-row items-center justify-between w-full">
                        <div className="w-full sm:absolute sm:left-6 sm:top-6 sm:w-[20%] text-center sm:text-left mb-4 sm:mb-0 flex flex-col gap-1">
                          <span className="text-[10px] sm:text-xs text-white font-bold uppercase tracking-widest block truncate">
                            {match.league}
                          </span>
                          {isHot && (
                            <span className="inline-block text-[10px] font-black text-red-500 bg-red-500/10 border border-red-500/30 px-2 py-0.5 rounded animate-pulse w-fit mx-auto sm:mx-0">
                              🔥 HOT VALUEBET
                            </span>
                          )}
                        </div>

                        <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-end z-10 mt-4 sm:mt-0">
                          <span className="font-bold text-lg text-right">{match.home_team}</span>
                          {match.home_logo ? <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain drop-shadow-md" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
                        </div>
                        
                        <div className="flex flex-col items-center justify-center px-4 w-full sm:w-1/5 my-4 sm:my-0 z-10">
                          <span className="text-xs text-slate-400 mb-2 font-medium">{new Date(match.match_date).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })}</span>
                          {['FINISHED', 'IN_PLAY', 'PAUSED'].includes(match.status) ? (
                            <span className={`px-4 py-1.5 rounded-xl font-black tracking-widest text-lg border transition-all ${scoreTheme}`}>
                              {match.home_score ?? 0} : {match.away_score ?? 0}
                            </span>
                          ) : (
                            <span className={`px-4 py-1.5 rounded-xl font-black tracking-widest text-sm border transition-all ${vsTheme}`}>VS</span>
                          )}
                        </div>

                        <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-start z-10">
                          {match.away_logo ? <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain drop-shadow-md" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
                          <span className="font-bold text-lg text-left">{match.away_team}</span>
                        </div>
                      </div>

                      {/* --- 4. KONTENER DOLNY (TEKST ANALIZY DLA GOOGLE) --- */}
                      {previewText && (
                        <div className="w-full mt-6 pt-5 border-t border-slate-800/50">
                          <p className="text-sm text-slate-400 line-clamp-[8] leading-relaxed">
                            {previewText}
                          </p>
                          <span className={`text-xs font-bold mt-3 inline-block transition-colors ${isHot ? 'text-red-500 group-hover:text-red-400' : 'text-emerald-500 group-hover:text-emerald-400'}`}>
                            Czytaj pełną analizę &rarr;
                          </span>
                        </div>
                      )}

                    </Link>
                  );
                })}
              </div>
            </div>
          ))
        )}

        {/* ========================================== */}
        {/* --- SEKCJA FAQ DLA GOOGLE ADSENSE --- */}
        {/* ========================================== */}
        <section className="mt-24 pt-12 border-t border-slate-800/80">
          <h2 className="text-3xl font-black text-slate-200 mb-8 text-center tracking-wide">
            Często zadawane pytania (FAQ)
          </h2>
          <div className="space-y-4">
            
            <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl hover:border-slate-700 transition-colors">
              <h3 className="text-emerald-400 font-bold text-lg mb-2">Jak działa sztuczna inteligencja na Sports Platform?</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Nasz autorski system opiera się na zaawansowanych modelach językowych, które w czasie rzeczywistym analizują twarde dane z boiska. Zamiast opierać się na intuicji, AI przetwarza informacje o potwierdzonych składach, brakach kadrowych oraz statystykach xG (oczekiwanych goli), dostarczając w 100% obiektywne i matematycznie uzasadnione analizy meczowe.
              </p>
            </div>

            <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl hover:border-slate-700 transition-colors">
              <h3 className="text-emerald-400 font-bold text-lg mb-2">Czym jest "Valuebet" (Gorący Typ) i jak go obliczamy?</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Valuebet to sytuacja, w której nasze algorytmy wyliczają, że prawdopodobieństwo wystąpienia danego zdarzenia jest wyższe, niż sugerują to kursy wystawione przez bukmachera. System mnoży pewność sztucznej inteligencji przez aktualny kurs rynkowy. Jeśli wynik równania matematycznego wykazuje przewagę gracza nad marżą bukmachera, system automatycznie oznacza mecz czerwoną etykietą "🔥 HOT VALUEBET".
              </p>
            </div>

            <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl hover:border-slate-700 transition-colors">
              <h3 className="text-emerald-400 font-bold text-lg mb-2">Czy analizy i statystyki na stronie są darmowe?</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Tak, naszą misją jest dostarczanie najwyższej jakości analiz sportowych bez ukrytych opłat. Wszystkie przedmeczowe typy wynikowe, dostęp do historii sprawdzalności algorytmu oraz głębokie statystyki meczowe są w pełni darmowe dla wszystkich użytkowników naszej platformy.
              </p>
            </div>

            <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl hover:border-slate-700 transition-colors">
              <h3 className="text-emerald-400 font-bold text-lg mb-2">Jak często aktualizowane są mecze w systemie?</h3>
              <p className="text-slate-400 text-sm leading-relaxed">
                Kalendarz spotkań oraz wyniki na żywo synchronizują się z naszymi serwerami 24 godziny na dobę. Przedmeczowe analizy AI są generowane dynamicznie na podstawie najświeższych doniesień z rynku, dzięki czemu zawsze opierają się na aktualnej sytuacji kadrowej i najnowszych wahaniach kursów bukmacherskich.
              </p>
            </div>

          </div>
        </section>

        {/* ========================================== */}
        {/* --- STOPKA (FOOTER) Z WYMOGAMI PRAWNYMI --- */}
        {/* ========================================== */}
        <footer className="mt-20 pt-10 border-t border-slate-800/80 pb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10 text-center md:text-left">
            
            {/* O nas */}
            <div>
              <h4 className="text-white font-bold mb-4">Sports Platform</h4>
              <p className="text-slate-500 text-xs leading-relaxed">
                Innowacyjne narzędzie analityczne dla fanów sportu. Wykorzystujemy potęgę sztucznej inteligencji, by dostarczać najbardziej precyzyjne prognozy i wykrywać przewagi rynkowe na podstawie twardych danych.
              </p>
            </div>

            {/* Linki prawne i nawigacja */}
            <div className="flex flex-col space-y-2">
              <h4 className="text-white font-bold mb-2">Nawigacja i regulaminy</h4>
              <Link href="/privacy-policy" className="text-slate-400 text-sm hover:text-emerald-400 transition-colors">Polityka Prywatności</Link>
              <Link href="/terms" className="text-slate-400 text-sm hover:text-emerald-400 transition-colors">Regulamin Serwisu</Link>
              <Link href="/contact" className="text-slate-400 text-sm hover:text-emerald-400 transition-colors">Kontakt z administracją</Link>
              <Link href="/history" className="text-slate-400 text-sm hover:text-emerald-400 transition-colors">Historia skuteczności</Link>
            </div>

            {/* Ostrzeżenie (Disclaimer) */}
            <div>
              <h4 className="text-white font-bold mb-4">Ważna informacja</h4>
              <p className="text-slate-500 text-xs leading-relaxed bg-slate-900/50 p-3 rounded-xl border border-slate-800/80">
                Serwis ma charakter wyłącznie informacyjny i analityczny. Nie namawiamy do hazardu. Zakłady bukmacherskie wiążą się z ryzykiem utraty kapitału. Uczestnictwo w nielegalnych grach hazardowych jest karane. Graj odpowiedzialnie.
              </p>
            </div>

          </div>

          <div className="text-xs text-slate-600 text-center border-t border-slate-800/50 pt-6">
            © {new Date().getFullYear()} Sports Platform. Wszelkie prawa zastrzeżone.
          </div>
        </footer>

      </div>
    </main>
  );
}