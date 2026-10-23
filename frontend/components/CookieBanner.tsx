'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Sprawdzamy, czy użytkownik podjął już decyzję
    const consent = localStorage.getItem('cookie_consent');
    if (!consent) {
      setIsVisible(true);
    }
  }, []);

  const acceptCookies = () => {
    localStorage.setItem('cookie_consent', 'accepted');
    setIsVisible(false);
  };

  const rejectCookies = () => {
    localStorage.setItem('cookie_consent', 'rejected');
    setIsVisible(false);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-slate-950 border-t border-slate-800 p-4 md:p-6 z-50 shadow-[0_-10px_40px_rgba(0,0,0,0.5)]">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="text-slate-400 text-sm md:text-base leading-relaxed">
          <p>
            Wykorzystujemy pliki cookie (ciasteczka) w celach analitycznych, do personalizacji treści oraz prawidłowego wyświetlania reklam (Google AdSense). 
            Klikając „Akceptuję”, wyrażasz zgodę na ich użycie. Szczegóły znajdziesz w naszej <Link href="/polityka-prywatnosci" className="text-emerald-400 font-semibold hover:text-emerald-300 transition-colors">Polityce Prywatności</Link>.
          </p>
        </div>
        <div className="flex gap-3 shrink-0 w-full md:w-auto justify-end">
          <button 
            onClick={rejectCookies} 
            className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 rounded-xl text-sm font-bold transition-colors w-full md:w-auto"
          >
            Odrzuć
          </button>
          <button 
            onClick={acceptCookies} 
            className="px-5 py-2.5 bg-emerald-500/10 border border-emerald-500/30 hover:bg-emerald-500/20 text-emerald-400 rounded-xl text-sm font-bold transition-colors w-full md:w-auto"
          >
            Akceptuję
          </button>
        </div>
      </div>
    </div>
  );
}
