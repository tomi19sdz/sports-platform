'use client';

import React, { useState } from 'react';

// Określamy, jak wygląda pojedyncze wideo
interface Video {
  id: number;
  video_url: string;
}

// Określamy, że nasze zakładki muszą otrzymać listę filmów
interface MatchTabsProps {
  videos: Video[];
}

// Mała funkcja, która wyciąga ID filmu z linku YouTube (np. ze znaku "=" lub z "youtu.be/")
const getYouTubeId = (url: string) => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  return (match && match[2].length === 11) ? match[2] : null;
};

export default function MatchTabs({ videos }: MatchTabsProps) {
  const [activeTab, setActiveTab] = useState('chat');

  return (
    <>
      <div className="flex border-b border-slate-800 mb-8">
        <button 
          onClick={() => setActiveTab('chat')}
          className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'chat' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}
        >
          Czat na żywo
        </button>
        <button 
          onClick={() => setActiveTab('video')}
          className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'video' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}
        >
          Wideo
        </button>
        <button 
          onClick={() => setActiveTab('analysis')}
          className={`py-3 px-8 font-bold text-lg border-b-2 transition-colors ${activeTab === 'analysis' ? 'border-emerald-500 text-emerald-500' : 'border-transparent text-slate-500 hover:text-slate-300'}`}
        >
          Analizy
        </button>
      </div>
      
      <div className="bg-slate-950/50 rounded-2xl min-h-[400px] p-6 border border-slate-800/50 flex flex-col items-center justify-center text-slate-400 font-medium">
        
        {activeTab === 'chat' && <div>Tutaj wkrótce pojawi się okno czatu na żywo...</div>}
        
        {/* Nowa, dynamiczna zakładka Wideo */}
        {activeTab === 'video' && (
          <div className="w-full h-full flex flex-col items-center justify-center">
            {videos && videos.length > 0 ? (
              videos.map((video) => {
                const videoId = getYouTubeId(video.video_url);
                return videoId ? (
                  <div key={video.id} className="w-full max-w-4xl aspect-video rounded-xl overflow-hidden shadow-2xl border border-slate-700/50 bg-black">
                    <iframe
                      width="100%"
                      height="100%"
                      src={`https://www.youtube.com/embed/${videoId}`}
                      title="YouTube video player"
                      frameBorder="0"
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                      allowFullScreen
                    ></iframe>
                  </div>
                ) : (
                  <div key={video.id} className="text-rose-400 bg-rose-950/30 p-4 rounded-lg">
                    Nieprawidłowy link YouTube: {video.video_url}
                  </div>
                );
              })
            ) : (
              <div className="text-slate-500 text-lg">
                Ten mecz nie ma jeszcze przypisanego materiału wideo.
              </div>
            )}
          </div>
        )}
        
        {activeTab === 'analysis' && <div>Tutaj dodamy formularz do pisania analiz sportowych...</div>}
        
      </div>
    </>
  );
}