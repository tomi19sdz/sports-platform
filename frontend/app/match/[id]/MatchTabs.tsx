'use client';

import React, { useState, useEffect } from 'react';

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
  
  // Stany dla Analiz
  const [analysisText, setAnalysisText] = useState('');
  const [localAnalyses, setLocalAnalyses] = useState<Analysis[]>(initialAnalyses || []);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Stany dla Czatu
  const [chatMessages, setChatMessages] = useState<{id: number, text: string, author: string}[]>([]);
  const [chatInput, setChatInput] = useState('');
  const [nickname, setNickname] = useState('');

  // --- ZAPIS GLOBALNY: Pobieranie wiadomości z Django ---
  const fetchChatMessages = async () => {
    try {
      const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${matchId}/chat/`);
      if (res.ok) {
        const data = await res.json();
        setChatMessages(data);
      }
    } catch (error) {
      console.error('Błąd pobierania czatu:', error);
    }
  };

  // Uruchom pobieranie czatu przy załadowaniu oraz odświeżaj co 3 sekundy (Live Chat)
  useEffect(() => {
    fetchChatMessages();
    const interval = setInterval(fetchChatMessages, 3000);
    return () => clearInterval(interval);
  }, [matchId]);


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
        alert('Twoja analiza została wysłana i oczekuje na zatwierdzenie przez administratora.');
        setAnalysisText(''); 
      } else {
        alert('Wystąpił błąd podczas dodawania analizy.');
      }
    } catch (error) {
      alert('Błąd połączenia z serwerem.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // --- ZAPIS GLOBALNY: Wysyłanie wiadomości do Django ---
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;
    
    const currentNickname = nickname.trim() !== '' ? nickname.trim() : 'Anonim';
    const textToSend = chatInput;
    
    // Natychmiastowo czyścimy pole tekstowe po kliknięciu
    setChatInput('');
    
    try {
      const res = await fetch(`https://tomi19sdz.pythonanywhere.com/api/matches/${matchId}/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ author: currentNickname, text: textToSend }),
      });

      if (res.ok) {
        // Po udanym wysłaniu od razu pobieramy odświeżoną listę z serwera
        fetchChatMessages();
      }
    } catch (error) {
      console.error('Błąd wysyłania wiadomości:', error);
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
        
        {/* ZAKŁADKA CZAT */}
        {activeTab === 'chat' && (
          <div className="flex flex-col h-[400px]">
            <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2">
              {chatMessages.length === 0 ? (
                <div className="text-center text-slate-500 mt-20 flex flex-col items-center">
                  <span className="text-4xl mb-3">💬</span>
                  <p>Brak wiadomości. Bądź pierwszy!</p>
                </div>
              ) : (
                chatMessages.map((msg) => (
                  <div key={msg.id} className="bg-emerald-600/20 border border-emerald-500/30 p-3 rounded-2xl rounded-tr-none max-w-[80%] ml-auto flex flex-col">
                    <span className="text-xs text-emerald-400 font-bold mb-1">{msg.author}</span>
                    <p className="text-slate-100">{msg.text}</p>
                  </div>
                ))
              )}
            </div>
            
            <div className="flex flex-col space-y-3 mt-auto">
              <input 
                type="text" 
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder="Twój nick (opcjonalnie)" 
                className="w-1/2 md:w-1/3 bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-emerald-500 transition-colors"
              />
              <div className="flex space-x-3">
                <input 
                  type="text" 
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendChatMessage()}
                  placeholder="Napisz wiadomość na czacie..." 
                  className="flex-1 bg-slate-900 border border-slate-700 rounded-xl p-4 text-white focus:outline-none focus:border-emerald-500 transition-colors"
                />
                <button 
                  onClick={sendChatMessage}
                  className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-8 rounded-xl transition-all shadow-[0_0_15px_rgba(0,223,129,0.2)]"
                >
                  Wyślij
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ZAKŁADKA WIDEO */}
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

        {/* ZAKŁADKA ANALIZY */}
        {activeTab === 'analysis' && (
          <div className="flex flex-col w-full max-w-4xl mx-auto space-y-8">
            <div className="bg-slate-900 border border-slate-700 p-4 rounded-xl">
              <h3 className="text-emerald-400 font-bold mb-3">Dodaj analizę:</h3>
              <textarea 
                className="w-full bg-slate-800 border border-slate-600 rounded-lg p-3 text-slate-200 min-h-[120px]" 
                value={analysisText} 
                onChange={(e) => setAnalysisText(e.target.value)} 
              />
              <button onClick={submitAnalysis} disabled={isSubmitting} className="mt-3 bg-emerald-600 text-white font-bold py-2 px-6 rounded-lg">Wyślij</button>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4">Dodane analizy:</h3>
              {localAnalyses.map((a) => (
                <div key={a.id} className="bg-slate-800/50 p-4 rounded-lg mb-4 whitespace-pre-wrap">{a.content}</div>
              ))}
            </div>
          </div>
        )}
      </div>
    </>
  );
}