'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';

export default function HomePage() {
  const [matches, setMatches] = useState({});
  const [activeTab, setActiveTab] = useState('nadchodzace');

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        // Pobieramy dane z serwera, upewniając się, że nie są zapisane w cache
        const res = await fetch('https://tomi19sdz.pythonanywhere.com/api/matches/', {
          cache: 'no-store'
        });
        const data = await res.json();
        setMatches(data);
      } catch (error) {
        console.error('Błąd pobierania meczów:', error);
      }
    };
    fetchMatches();
  }, []);

  // KRYTYCZNA ZMIANA: Ustawiamy "dzisiaj" na sam początek dnia (00:00:00).
  // Dzięki temu dzisiejsze mecze nie uciekną do historii przed północą.
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const upcomingMatches: Record<string, any> = {};
  const historyMatches: Record<string, any> = {};

  // Rozdzielamy mecze na zakładki
  Object.entries(matches).forEach(([dateString, dailyMatches]) => {
    const matchDate = new Date(dateString);
    matchDate.setHours(0, 0, 0, 0); // Porównujemy całe dnie, a nie konkretne godziny

    if (matchDate >= today) {
      upcomingMatches[dateString] = dailyMatches;
    } else {
      historyMatches[dateString] = dailyMatches;
    }
  });

  const displayMatches = activeTab === 'nadchodzace' ? upcomingMatches : historyMatches;
  const hasMatches = Object.keys(displayMatches).length > 0;

  return (
    <div className="min-h-screen bg-[#0a0f16] text-slate-200 p-8 flex flex-col items-center">
      <h1 className="text-4xl md:text-5xl font-black text-white mb-12 tracking-wide uppercase mt-10">
        Terminarz Spotkań
      </h1>
      
      {/* Przyciski nawigacyjne */}
      <div className="flex space-x-4 mb-16">
        <button 
          onClick={() => setActiveTab('nadchodzace')} 
          className={`py-3 px-8 font-bold rounded-full transition-all duration-300 ${
            activeTab === 'nadchodzace' 
              ? 'bg-[#00df81] text-black shadow-[0_0_20px_rgba(0,223,129,0.4)]' 
              : 'bg-[#1a2332] text-slate-300 hover:bg-[#232f43]'
          }`}
        >
          Nadchodzące
        </button>
        <button 
          onClick={() => setActiveTab('historia')} 
          className={`py-3 px-8 font-bold rounded-full transition-all duration-300 ${
            activeTab === 'historia' 
              ? 'bg-[#1a2332] text-white ring-2 ring-slate-600' 
              : 'bg-[#1a2332] text-slate-300 hover:bg-[#232f43]'
          }`}
        >
          Historia
        </button>
      </div>

      {/* Lista meczów */}
      <div className="w-full max-w-3xl">
        {!hasMatches ? (
          <div className="text-center text-[#64748b] text-xl mt-10">
            {activeTab === 'nadchodzace' ? 'Brak nadchodzących meczów.' : 'Brak meczów w historii.'}
          </div>
        ) : (
          Object.entries(displayMatches).map(([date, dailyMatches]: [string, any]) => (
            <div key={date} className="mb-12">
              <h2 className="text-xl font-bold text-[#64748b] mb-6 border-b border-[#1e293b] pb-2">
                {date}
              </h2>
              <div className="space-y-4">
                {dailyMatches.map((match: any) => (
                  <div key={match.id} className="bg-[#111827] border border-[#1e293b] p-6 rounded-2xl flex justify-between items-center hover:border-[#00df81]/50 transition-colors">
                    <div className="flex items-center space-x-6">
                      <span className="text-2xl font-bold text-white">{match.home_team}</span>
                      <span className="text-slate-500 font-medium">vs</span>
                      <span className="text-2xl font-bold text-white">{match.away_team}</span>
                    </div>
                    {/* Zmień '/matches/' na swój prawdziwy link do szczegółów, jeśli jest inny */}
                    <Link href={`/matches/${match.id}`} className="bg-[#1e293b] hover:bg-[#2dd4bf] hover:text-black text-slate-300 py-2 px-6 rounded-xl font-bold transition-all">
                      Zobacz
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}