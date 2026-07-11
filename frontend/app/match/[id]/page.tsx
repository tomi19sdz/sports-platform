import React from 'react';
import Link from 'next/link';
import MatchTabs from './MatchTabs';

interface Video { id: number; video_url: string; }
interface Analysis { id: number; content: string; }
interface Match {
  id: number;
  home_team: string;
  away_team: string;
  match_date: string;
  videos: Video[];
  analyses: Analysis[];
}

async function getMatch(id: string): Promise<Match> {
  const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${id}/`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Błąd pobierania');
  return res.json();
}

export default async function MatchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const match = await getMatch(id);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-5xl mx-auto">
        <Link href="/" className="text-emerald-500 mb-8 inline-block">&larr; Wróć</Link>
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8">
          <h1 className="text-4xl font-extrabold text-center mb-10">
            {match.home_team} <span className="text-emerald-500">VS</span> {match.away_team}
          </h1>
          <MatchTabs matchId={match.id} videos={match.videos || []} analyses={match.analyses || []} />
        </div>
      </div>
    </main>
  );
}