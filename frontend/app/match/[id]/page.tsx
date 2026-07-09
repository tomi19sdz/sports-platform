import React from 'react';
import Link from 'next/link';
import MatchTabs from './MatchTabs';

// Aktualizujemy budowę meczu, by uwzględniała filmy!
interface Video {
  id: number;
  video_url: string;
}

interface Match {
  id: number;
  home_team: string;
  away_team: string;
  match_date: string;
  videos: Video[]; // <--- Tu dodaliśmy filmy z bazy Django
}

async function getMatch(id: string): Promise<Match> {
  const res = await fetch(`http://127.0.0.1:8000/api/matches/${id}/`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Nie udało się pobrać meczu.');
  return res.json();
}

export default async function MatchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const match = await getMatch(id);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8 font-sans">
      <div className="max-w-5xl mx-auto">
        <Link href="/" className="text-emerald-500 hover:text-emerald-400 font-semibold mb-8 inline-block transition-colors">
          &larr; Wróć do listy spotkań
        </Link>
        
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-2xl">
          <h1 className="text-4xl font-extrabold text-center mb-10 tracking-wide">
            {match.home_team} <span className="text-emerald-500 text-2xl mx-6 font-black">VS</span> {match.away_team}
          </h1>
          
          {/* Przekazujemy listę filmów do komponentu zakładek (jeśli pusta, wysyłamy pustą tablicę []) */}
          <MatchTabs videos={match.videos || []} />

        </div>
      </div>
    </main>
  );
}