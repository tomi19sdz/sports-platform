import React from 'react';

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-2xl mx-auto mt-10 text-center">
        <h1 className="text-4xl font-black text-white mb-4">Kontakt</h1>
        <p className="text-slate-400 text-lg mb-8">
          Masz pytania dotyczące naszych analiz meczowych, współpracy lub funkcjonowania platformy? Zespół Sports Platform jest do Twojej dyspozycji.
        </p>

        <div className="bg-slate-900/40 p-8 rounded-2xl border border-slate-800/80">
          <h2 className="text-2xl font-bold text-emerald-400 mb-4">Napisz do nas</h2>
          <p className="text-slate-300 mb-2">Adres e-mail:</p>
          <a href="mailto:kontakt@twojadomena.pl" className="text-xl font-bold text-white hover:text-emerald-400 transition-colors">
            kontakt@twojadomena.pl
          </a>
          <p className="text-slate-500 mt-6 text-sm">
            Staramy się odpowiadać na wszystkie zapytania w ciągu 24-48 godzin.
          </p>
        </div>
      </div>
    </main>
  );
}