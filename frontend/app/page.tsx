import Link from 'next/link';
import React from 'react';

// Zaktualizowany interfejs z backendu (dodano wyniki i status)
interface Match {
  id: number;
  home_team: string;
  away_team: string;
  home_logo: string | null;
  away_logo: string | null;
  match_date: string;
  home_score: number | null;
  away_score: number | null;
  status: string;
}

// Funkcja pobierająca mecze z Django
async function getMatches() {
  const res = await fetch('https://tomi19sdz.pythonanywhere.com/api/matches/', {
    next: { revalidate: 60 } 
  });
  
  if (!res.ok) {
    return {};
  }
  
  return res.json() as Promise<Record<string, Match[]>>;
}

export default async function HomePage() {
  const groupedMatches = await getMatches();

  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center mt-10">
          <h1 className="text-5xl font-black text-white mb-4 tracking-tight">
            Sports <span className="text-emerald-500">Platform</span>
          </h1>
          <p className="text-slate-400 text-lg">Nadchodzące spotkania, wyniki na żywo i analizy</p>
        </header>

        {Object.keys(groupedMatches).length === 0 ? (
          <div className="text-center text-slate-500 mt-20 flex flex-col items-center">
            <span className="text-6xl mb-4">🏟️</span>
            <p className="text-xl">Brak meczów w bazie danych.</p>
            <p className="text-sm mt-2">Zaktualizuj bazę w panelu administratora.</p>
          </div>
        ) : (
          Object.entries(groupedMatches).map(([date, matches]) => (
            <div key={date} className="mb-12">
              <h2 className="text-2xl font-bold text-emerald-400 mb-6 border-b border-slate-800/80 pb-3 flex items-center">
                <span className="bg-emerald-500/10 text-emerald-500 px-3 py-1 rounded-lg text-sm mr-3 border border-emerald-500/20">
                  📅
                </span>
                {date}
              </h2>
              
              <div className="grid gap-4">
                {matches.map((match) => (
                  <Link 
                    key={match.id} 
                    href={`/match/${match.id}`}
                    className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 hover:border-emerald-500/50 hover:bg-slate-800/60 hover:-translate-y-1 transition-all duration-300 flex flex-col sm:flex-row items-center justify-between group shadow-lg shadow-black/20"
                  >
                    {/* Gospodarz */}
                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-end">
                      <span className="font-bold text-lg text-right">{match.home_team}</span>
                      {match.home_logo ? (
                        <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain drop-shadow-md" />
                      ) : (
                        <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>
                      )}
                    </div>
                    
                    {/* Środek (Godzina / Wynik / VS) */}
                    <div className="flex flex-col items-center justify-center px-4 w-full sm:w-1/5 my-4 sm:my-0">
                      <span className="text-xs text-slate-400 mb-2 font-medium">
                        {new Date(match.match_date).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })}
                      </span>
                      
                      {/* Magia wyników: jeśli mecz jest zakończony lub w trakcie, pokazujemy cyfry */}
                      {['FINISHED', 'IN_PLAY', 'PAUSED'].includes(match.status) ? (
                        <span className="bg-emerald-500/10 px-4 py-1.5 rounded-xl text-emerald-400 font-black tracking-widest text-lg border border-emerald-500/30 group-hover:border-emerald-500/60 transition-all">
                          {match.home_score !== null ? match.home_score : 0} : {match.away_score !== null ? match.away_score : 0}
                        </span>
                      ) : (
                        <span className="bg-slate-950 px-4 py-1.5 rounded-xl text-slate-400 font-black tracking-widest text-sm border border-slate-700/50 group-hover:text-emerald-500 group-hover:border-emerald-500/50 transition-all">
                          VS
                        </span>
                      )}
                    </div>

                    {/* Gość */}
                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-start">
                      {match.away_logo ? (
                        <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain drop-shadow-md" />
                      ) : (
                        <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>
                      )}
                      <span className="font-bold text-lg text-left">{match.away_team}</span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </main>
  );
}