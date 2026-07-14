import Link from 'next/link';
import React from 'react';

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

async function getMatches() {
  const res = await fetch('https://tomi19sdz.pythonanywhere.com/api/matches/', {
    next: { revalidate: 60 } 
  });
  if (!res.ok) return {};
  return res.json() as Promise<Record<string, Match[]>>;
}

export default async function HistoryPage() {
  const groupedMatches = await getMatches();
  const todayStr = new Date().toISOString().split('T')[0];
  
  // Filtrujemy TYLKO mecze zakończone/przeszłe (data mniejsza niż dzisiejsza)
  const pastMatches = Object.entries(groupedMatches).filter(([date]) => date < todayStr);
  
  // Odwracamy kolejność, aby najświeższa historia była na samej górze
  pastMatches.sort((a, b) => b[0].localeCompare(a[0]));

  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-10 text-center mt-10">
          <h1 className="text-5xl font-black text-white mb-4 tracking-tight">
            Sports <span className="text-slate-500">History</span>
          </h1>
          <p className="text-slate-400 text-lg mb-8">Archiwum zakończonych spotkań</p>
          
          {/* Nawigacja / Zakładki (Odwrotne kolory) */}
          <div className="flex justify-center space-x-4">
            <Link href="/" className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full font-bold hover:bg-slate-700 transition-colors">
              Nadchodzące
            </Link>
            <Link href="/history" className="px-6 py-2 bg-emerald-600 text-white rounded-full font-bold shadow-lg shadow-emerald-500/20">
              Historia
            </Link>
          </div>
        </header>

        {pastMatches.length === 0 ? (
          <div className="text-center text-slate-500 mt-20 flex flex-col items-center">
            <span className="text-6xl mb-4">📜</span>
            <p className="text-xl">Brak historii meczów.</p>
          </div>
        ) : (
          pastMatches.map(([date, matches]) => (
            <div key={date} className="mb-12 opacity-80 hover:opacity-100 transition-opacity">
              <h2 className="text-2xl font-bold text-slate-400 mb-6 border-b border-slate-800/80 pb-3 flex items-center">
                <span className="bg-slate-800 text-slate-400 px-3 py-1 rounded-lg text-sm mr-3">📅</span>
                {date}
              </h2>
              
              <div className="grid gap-4">
                {matches.map((match) => (
                  <Link key={match.id} href={`/match/${match.id}`} className="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 hover:border-slate-500/50 hover:bg-slate-800/60 transition-all duration-300 flex flex-col sm:flex-row items-center justify-between group">
                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-end filter grayscale group-hover:grayscale-0 transition-all">
                      <span className="font-bold text-lg text-right">{match.home_team}</span>
                      {match.home_logo ? <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
                    </div>
                    
                    <div className="flex flex-col items-center justify-center px-4 w-full sm:w-1/5 my-4 sm:my-0">
                      {['FINISHED', 'IN_PLAY', 'PAUSED'].includes(match.status) ? (
                        <span className="bg-slate-800 px-4 py-1.5 rounded-xl text-slate-300 font-black tracking-widest text-lg border border-slate-700">
                          {match.home_score ?? 0} : {match.away_score ?? 0}
                        </span>
                      ) : (
                        <span className="bg-slate-950 px-4 py-1.5 rounded-xl text-slate-600 font-black tracking-widest text-sm border border-slate-800">VS</span>
                      )}
                    </div>

                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-start filter grayscale group-hover:grayscale-0 transition-all">
                      {match.away_logo ? <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
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