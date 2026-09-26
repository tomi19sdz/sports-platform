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
  confidence_score?: number;
  is_valuebet?: boolean;
  value_percentage?: number;
}

// Interfejs dla pobieranych wiadomości
interface NewsItem {
  title: string;
  link: string;
  pubDate: string;
}

async function getMatch(id: string): Promise<Match> {
  const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${id}/`, { cache: 'no-store' });
  if (!res.ok) throw new Error('Błąd pobierania meczu');
  return res.json();
}

// NOWA FUNKCJA: Pobieranie najświeższych wiadomości z Google News (bez kluczy API)
async function getNews(homeTeam: string, awayTeam: string): Promise<NewsItem[]> {
  try {
    const query = encodeURIComponent(`${homeTeam} ${awayTeam} piłka nożna`);
    const rssUrl = `https://news.google.com/rss/search?q=${query}&hl=pl&gl=PL&ceid=PL:pl`;
    // Używamy darmowego konwertera rss2json, żeby łatwo odczytać dane z Google News
    const res = await fetch(`https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`, { 
      next: { revalidate: 3600 } // Odświeżaj newsy co godzinę
    });
    
    if (!res.ok) return [];
    const data = await res.json();
    return data.items ? data.items.slice(0, 3) : []; // Bierzemy tylko 3 najnowsze
  } catch (error) {
    console.error("Błąd pobierania wiadomości:", error);
    return [];
  }
}

export async function generateMetadata({ params }: { params: Promise<{ id: string }> }): Promise<Metadata> {
  const { id } = await params;
  const match = await getMatch(id);

  return {
    title: `${match.home_team} vs ${match.away_team} | Sports Platform`,
    description: `Sprawdź szczegóły meczu ${match.home_team} kontra ${match.away_team} w lidze ${match.league}. Najnowsze wiadomości, analizy AI i skróty wideo.`,
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
  
  // Pobieramy dane meczu i najświeższe newsy jednocześnie
  const match = await getMatch(id);
  const newsList = await getNews(match.home_team, match.away_team);

  // Dynamiczne style dla głównego kontenera i nagłówka
  const isHot = match.is_valuebet;
  const containerStyle = isHot 
    ? 'bg-slate-900 border-red-600 shadow-[0_0_30px_rgba(239,68,68,0.2)]' 
    : 'bg-slate-900 border-slate-800';
  const vsStyle = isHot ? 'text-red-500 drop-shadow-[0_0_10px_rgba(239,68,68,0.8)]' : 'text-emerald-500';

  // Generator linku do automatycznego wyszukiwania skrótów na YouTube
  const youtubeSearchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(`${match.home_team} vs${match.away_team} skrót meczu highlights`)}`;

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 p-8">
      <div className="max-w-5xl mx-auto">
        <Link href="/" className="text-emerald-500 mb-8 inline-block hover:text-emerald-400 transition-colors font-semibold tracking-wide">
          &larr; Wróć do listy meczów
        </Link>
        
        <div className={`border rounded-3xl p-8 transition-all duration-700 ${containerStyle}`}>
          
          <div className="text-center mb-4">
             <span className="text-xs text-slate-400 font-black uppercase tracking-widest bg-slate-950/50 px-4 py-1.5 rounded-full border border-slate-800/80">
                {match.league}
             </span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-center mb-8 tracking-tight">
            {match.home_team} <span className={`mx-3 ${vsStyle}`}>VS</span> {match.away_team}
          </h1>

          {/* --- WIZUALIZACJA VALUEBET I PEWNOŚCI AI --- */}
          <div className={`flex flex-col items-center justify-center gap-3 mb-8 p-6 rounded-2xl border max-w-md mx-auto shadow-inner transition-colors duration-500 ${isHot ? 'bg-red-950/20 border-red-900/50' : 'bg-slate-950/50 border-slate-800/80'}`}>
            <div className="flex items-center gap-4 w-full">
              <span className="text-sm font-bold text-slate-400 whitespace-nowrap">Pewność AI:</span>
              <div className="flex-1 bg-slate-800/80 rounded-full h-3 overflow-hidden border border-slate-700/50">
                <div 
                  className={`${isHot ? 'bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.6)]' : 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.4)]'} h-full rounded-full transition-all duration-1000`} 
                  style={{ width: `${match.confidence_score || 50}%` }}
                ></div>
              </div>
              <span className={`text-base font-black ${isHot ? 'text-red-400' : 'text-emerald-400'}`}>
                {match.confidence_score || 50}%
              </span>
            </div>

            {isHot && (
              <div className="mt-3 inline-flex items-center gap-2 px-5 py-2 rounded-full text-sm font-black bg-red-500/10 text-red-500 border border-red-500/50 shadow-[0_0_20px_rgba(239,68,68,0.3)] animate-pulse">
                🔥 VALUEBET WYKRYTY: +{match.value_percentage}%
              </div>
            )}
          </div>
          {/* --- KONIEC WIZUALIZACJI --- */}

          {/* --- SZYBKIE AKCJE (YOUTUBE) --- */}
          <div className="flex justify-center mb-12">
            <a 
              href={youtubeSearchUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="group flex items-center gap-3 bg-slate-900 border border-red-900/30 hover:border-red-500/80 hover:bg-red-950/30 px-6 py-3 rounded-xl transition-all shadow-lg hover:shadow-[0_0_20px_rgba(239,68,68,0.2)]"
            >
              <div className="bg-red-600 group-hover:bg-red-500 text-white rounded-full p-1.5 transition-colors">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/></svg>
              </div>
              <span className="font-bold text-slate-300 group-hover:text-white transition-colors">Obejrzyj skrót na YouTube</span>
            </a>
          </div>

          {/* --- SEKCJA WIADOMOŚCI GOOGLE (SEO) --- */}
          {newsList.length > 0 && (
            <div className="mb-12">
              <h2 className="text-xl font-bold text-emerald-400 mb-6 flex items-center gap-2 border-b border-slate-800/80 pb-3">
                <span className="bg-emerald-500/10 text-emerald-500 p-1.5 rounded-lg border border-emerald-500/20">📰</span>
                Najświeższe wiadomości
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {newsList.map((news, index) => {
                  // Wyciągamy źródło i krótką datę
                  const date = new Date(news.pubDate).toLocaleDateString('pl-PL', { day: '2-digit', month: 'short' });
                  return (
                    <a 
                      key={index} 
                      href={news.link} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl hover:bg-slate-800/80 hover:border-emerald-500/30 transition-all flex flex-col justify-between group"
                    >
                      <h3 className="text-sm font-bold text-slate-300 group-hover:text-emerald-400 leading-snug line-clamp-3 mb-4 transition-colors">
                        {news.title}
                      </h3>
                      <div className="text-xs text-slate-500 font-medium">
                        Wiadomości Google • {date}
                      </div>
                    </a>
                  );
                })}
              </div>
            </div>
          )}

          {/* --- TWOJE ZAKŁADKI Z KOMPONENTU CLIENT-SIDE --- */}
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