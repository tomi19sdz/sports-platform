'use client';

import React, { useState } from 'react';

interface Video {
  id: number;
  video_url: string;
}

interface Analysis {
  id: number;
  content: string;
}

interface MatchTabsProps {
  matchId: number;
  videos: Video[];
  analyses: Analysis[];
}

const getYouTubeId = (url: string) => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

export default function MatchTabs({ matchId, videos, analyses: initialAnalyses }: MatchTabsProps) {
  const [activeTab, setActiveTab] = useState('chat');
  const [analysisText, setAnalysisText] = useState('');
  const [localAnalyses, setLocalAnalyses] = useState<Analysis[]>(initialAnalyses || []);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const submitAnalysis = async () => {
    if (!analysisText.trim()) return;
    setIsSubmitting(true);
    
    try {
      const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${matchId}/add_analysis/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: analysisText }),
      });

      if (res.ok) {
        // Zamiast dodawać do listy, pokazujemy tylko komunikat:
        alert('Twoja analiza została wysłana i oczekuje na zatwierdzenie przez administratora.');
        setAnalysisText(''); // Czyścimy pole tekstowe
      } else {
        alert('Wystąpił błąd podczas dodawania analizy.');
      }
    } catch (error) {
      alert('Błąd połączenia z serwerem.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <div className="flex border-b border-slate-800 mb-8">
        <button onClick={() => setActiveTab('chat')} className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'chat' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}>Czat</button>
        <button onClick={() => setActiveTab('video')} className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'video' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}>Wideo</button>
        <button onClick={() => setActiveTab('analysis')} className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'analysis' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}>Analizy</button>
      </div>
      
      <div className="bg-slate-950/50 rounded-2xl min-h-[400px] p-6 border border-slate-800/50 flex flex-col w-full text-slate-200">
        {activeTab === 'chat' && <div className="text-center text-slate-500 mt-20">Czat w przygotowaniu...</div>}
        {activeTab === 'video' && (
          <div className="w-full h-full flex flex-col items-center justify-center">
            {videos && videos.length > 0 ? videos.map((v) => {
              const id = getYouTubeId(v.video_url);
              return id ? (
                <div key={v.id} className="w-full max-w-4xl aspect-video rounded-xl overflow-hidden mb-6"><iframe width="100%" height="100%" src={`https://www.youtube.com/embed/${id}`} allowFullScreen></iframe></div>
              ) : null;
            }) : <div className="text-slate-500">Brak wideo.</div>}
          </div>
        )}
        {activeTab === 'analysis' && (
          <div className="flex flex-col w-full max-w-4xl mx-auto space-y-8">
            <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl">
              <h3 className="text-emerald-400 font-bold mb-3">Dodaj analizę:</h3>
              <textarea className="w-full bg-slate-800 border border-slate-600 rounded-lg p-3 text-slate-200" value={analysisText} onChange={(e) => setAnalysisText(e.target.value)} />
              <button onClick={submitAnalysis} disabled={isSubmitting} className="mt-3 bg-emerald-600 text-white font-bold py-2 px-6 rounded-lg">Wyślij</button>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Dodane analizy:</h3>
              {localAnalyses.map((a) => <div key={a.id} className="bg-slate-800/50 p-4 rounded-lg mb-4">{a.content}</div>)}
            </div>
          </div>
        )}
      </div>
    </>
  );
}