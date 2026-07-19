import Link from 'next/link';
import React from 'react';

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
        <header className="mb-10 text-center mt-10">
          <h1 className="text-5xl font-black text-white mb-4 tracking-tight">
            Sports <span className="text-emerald-500">Platform</span>
          </h1>
          <p className="text-slate-400 text-lg mb-8">Rozkład jazdy i wyniki na żywo</p>
          
          <div className="flex justify-center space-x-4">
            <Link href="/" className="px-6 py-2 bg-emerald-600 text-white rounded-full font-bold shadow-lg shadow-emerald-500/20">
              Nadchodzące
            </Link>
            <Link href="/history" className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full font-bold hover:bg-slate-700 transition-colors">
              Historia
            </Link>
            <Link href="/live-sport" className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full font-bold hover:bg-slate-700 transition-colors">
              Live Sport
            </Link>
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
                {matches.map((match) => (
                  <Link key={match.id} href={`/match/${match.id}`} className="relative bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 hover:border-emerald-500/50 hover:bg-slate-800/60 hover:-translate-y-1 transition-all duration-300 flex flex-col sm:flex-row items-center justify-between group shadow-lg shadow-black/20">
                    
                    {/* --- ZMIANA: LIGA NA LEWEJ STRONIE --- */}
                    {/* Na Desktopie pozycjonowana absolutnie po lewej, na Mobile ląduje u góry */}
                    <div className="w-full sm:absolute sm:left-6 sm:top-1/2 sm:-translate-y-1/2 sm:w-[20%] text-center sm:text-left mb-4 sm:mb-0">
                      <span className="text-[10px] sm:text-xs text-white font-bold uppercase tracking-widest block truncate">
                        {match.league}
                      </span>
                    </div>
                    {/* ------------------------------------ */}

                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-end z-10">
                      <span className="font-bold text-lg text-right">{match.home_team}</span>
                      {match.home_logo ? <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain drop-shadow-md" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
                    </div>
                    
                    <div className="flex flex-col items-center justify-center px-4 w-full sm:w-1/5 my-4 sm:my-0 z-10">
                      <span className="text-xs text-slate-400 mb-2 font-medium">{new Date(match.match_date).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit' })}</span>
                      {['FINISHED', 'IN_PLAY', 'PAUSED'].includes(match.status) ? (
                        <span className="bg-emerald-500/10 px-4 py-1.5 rounded-xl text-emerald-400 font-black tracking-widest text-lg border border-emerald-500/30 group-hover:border-emerald-500/60 transition-all">
                          {match.home_score ?? 0} : {match.away_score ?? 0}
                        </span>
                      ) : (
                        <span className="bg-slate-950 px-4 py-1.5 rounded-xl text-slate-400 font-black tracking-widest text-sm border border-slate-700/50 group-hover:text-emerald-500 group-hover:border-emerald-500/50 transition-all">VS</span>
                      )}
                    </div>

                    <div className="flex items-center space-x-4 w-full sm:w-2/5 justify-start z-10">
                      {match.away_logo ? <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain drop-shadow-md" /> : <div className="w-12 h-12 bg-slate-800 rounded-full flex items-center justify-center text-xs text-slate-500">Brak</div>}
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