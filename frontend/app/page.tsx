import React from 'react';
import Link from 'next/link';

interface Match {
  id: number;
  home_team: string;
  away_team: string;
  match_date: string;
  home_logo?: string; 
  away_logo?: string;
}

type GroupedMatches = {
  [date: string]: Match[];
};

async function getMatches(): Promise<GroupedMatches> {
  const res = await fetch('http://127.0.0.1:8000/api/matches/', { 
    cache: 'no-store'
  });
  
  if (!res.ok) {
    throw new Error('Nie udało się pobrać meczów.');
  }
  return res.json();
}

export default async function Home() {
  const matches = await getMatches();
  
  // Pobieramy dzisiejszą datę w formacie YYYY-MM-DD
  const todayStr = new Date().toISOString().split('T')[0];
  
  // Filtrujemy: zostawiamy tylko te daty, które są równe lub większe od dzisiaj
  const upcomingMatches = Object.entries(matches).filter(([date]) => date >= todayStr);

  return (
    <main className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-950 to-black font-sans text-slate-100 p-8">
      
      <div className="max-w-4xl mx-auto space-y-12 pt-12">
        <h1 className="text-5xl font-extrabold text-center mb-8 text-white drop-shadow-lg tracking-wide uppercase">
          Terminarz Spotkań
        </h1>

        {/* --- MENU NAWIGACYJNE --- */}
        <div className="flex justify-center gap-6 mb-12">
          <Link href="/" className="px-8 py-3 bg-emerald-500 text-slate-950 text-lg font-bold rounded-full shadow-[0_0_20px_rgba(16,185,129,0.4)] transition-all">
            Nadchodzące
          </Link>
          <Link href="/history" className="px-8 py-3 bg-slate-800/80 text-slate-300 text-lg font-bold rounded-full border border-slate-600 hover:bg-slate-700 hover:text-white transition-all">
            Historia
          </Link>
        </div>
        {/* ----------------------- */}
        
        <div className="space-y-12">
          {upcomingMatches.length === 0 ? (
            <p className="text-center text-slate-400 text-xl">Brak nadchodzących meczów.</p>
          ) : (
            upcomingMatches.map(([date, dailyMatches]) => (
              <div key={date}>
                <h2 className="text-2xl font-bold text-emerald-400 border-b border-emerald-500/30 pb-2 mb-6 uppercase tracking-widest text-center">
                  Mecze z dnia: {date}
                </h2>
                
                <div className="space-y-6">
                  {dailyMatches.map((match) => (
                    <Link 
                      href={`/match/${match.id}`}
                      key={match.id} 
                      className="bg-slate-900/60 backdrop-blur-md rounded-2xl shadow-2xl p-8 flex justify-between items-center border border-slate-700/50 hover:bg-slate-800/70 hover:border-emerald-500/50 transition-all duration-300 cursor-pointer block"
                    >
                      <div className="w-2/5 flex justify-end items-center gap-4">
                        <div className="text-3xl font-bold text-white tracking-wide text-right">
                          {match.home_team}
                        </div>
                        {match.home_logo && (
                          <img src={match.home_logo} alt={match.home_team} className="w-12 h-12 object-contain drop-shadow-md" />
                        )}
                      </div>
                      
                      <div className="w-1/5 flex justify-center">
                        <span className="bg-emerald-500 text-slate-950 text-base font-black px-6 py-2 rounded-full shadow-[0_0_15px_rgba(16,185,129,0.5)]">
                          VS
                        </span>
                      </div>
                      
                      <div className="w-2/5 flex justify-start items-center gap-4">
                        {match.away_logo && (
                          <img src={match.away_logo} alt={match.away_team} className="w-12 h-12 object-contain drop-shadow-md" />
                        )}
                        <div className="text-3xl font-bold text-white tracking-wide text-left">
                          {match.away_team}
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}