import React from 'react';
import Link from 'next/link';

export default function LiveSportPage() {
  return (
    <div className="min-h-screen bg-[#0a0f1d] flex flex-col items-center py-10 px-4">
      {/* Przycisk Wróć */}
      <div className="w-full max-w-5xl mb-4">
        <Link href="/" className="inline-flex items-center text-emerald-500 hover:text-emerald-400 font-bold transition-colors">
          <span className="mr-2">←</span> Wróć
        </Link>
      </div>

      {/* Nagłówek strony */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-2">
          Sports <span className="text-emerald-500">Live</span>
        </h1>
        <p className="text-gray-400">Wyniki spotkań na żywo z całego świata</p>
      </div>

      {/* Kontener na Twój widget */}
      <div className="w-full max-w-5xl bg-[#111827] rounded-xl shadow-lg border border-gray-800 p-2 md:p-4 overflow-hidden">
        <iframe 
          src="https://embed.soccersapi.com/widgets/ls-soccersapi/free.html?uid=6a5678adb115319341f6f5f2&widget-id=livescore&locale=pl&height=1200" 
          style={{ width: '100%', height: '1200px', minHeight: '1200px', border: 0, display: 'block' }} 
          loading="lazy" 
          referrerPolicy="strict-origin-when-cross-origin" 
          data-soccersapi-widget="v2-free"
        />
      </div>
    </div>
  );
}