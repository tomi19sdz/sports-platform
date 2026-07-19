import React from 'react';
import Link from 'next/link';
import MatchTabs from './MatchTabs';
import type { Metadata } from 'next';

interface Video { id: number; video_url: string; }
interface Analysis { id: number; content: string; }
interface Match {
  id: number;
  home_team: string;
  away_team: string;
  league: string;
  match_date: string;
  videos: Video[];
  analyses: Analysis[];
}

async function getMatch(id: string): Promise<Match> {
  const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${id}/`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Błąd pobierania');
  return res.json();
}

// Funkcja generująca meta tagi dla każdego meczu
export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  const match = await getMatch(id);

  return {
    title: `${match.home_team} vs ${match.away_team} | Sports Platform`,
    description: `Sprawdź szczegóły meczu ${match.home_team} kontra ${match.away_team} w lidze ${match.league}.`,
    openGraph: {
      title: `${match.home_team} vs ${match.away_team}`,
      description: `Analiza i wideo z meczu ${match.home_team} - ${match.away_team}`,
      url: `https://sportsplatform.pl/match/${id}`,
      type: 'website',
      siteName: 'Sports Platform',
    },
    twitter: {
      card: 'summary_large_image',
      title: `${match.home_team} vs ${match.away_team}`,
      description: `Wynik meczu na żywo: ${match.home_team} vs ${match.away_team}`,
    },
  };
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
          <MatchTabs 
            matchId={match.id} 
            league={match.league} 
            videos={match.videos || []} 
            analyses={match.analyses || []} 
          />
        </div>
      </div>
    </main>
  );
}