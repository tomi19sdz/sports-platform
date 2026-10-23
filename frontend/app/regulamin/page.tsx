import React from 'react';
import Link from 'next/link';

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-4xl mx-auto mt-10">
        <h1 className="text-4xl font-black text-white mb-8">Regulamin Serwisu</h1>
        
        <div className="space-y-6 text-slate-400 leading-relaxed bg-slate-900/40 p-8 rounded-2xl border border-slate-800/80 shadow-lg">
          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">1. Postanowienia ogólne</h2>
            <p>Niniejszy regulamin określa zasady korzystania z serwisu internetowego Sports Platform. Użytkownik korzystając z platformy akceptuje warunki niniejszego dokumentu.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">2. Charakter informacyjny serwisu</h2>
            <p>Wszystkie dane, statystyki oraz prognozy (w tym oznaczenia "Wysoka Pewność") publikowane na łamach Sports Platform mają charakter wyłącznie informacyjny, statystyczny i edukacyjny. Serwis nie jest firmą bukmacherską, nie organizuje gier losowych i nie pośredniczy w przyjmowaniu zakładów.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">3. Wyłączenie odpowiedzialności</h2>
            <p>Twórcy serwisu dokładają wszelkich starań, aby prezentowane dane z modeli matematycznych były precyzyjne, jednak nie ponoszą odpowiedzialności za błędy w statystykach czy zmianach kursów. Decyzje podejmowane na podstawie informacji z serwisu użytkownik podejmuje wyłącznie na własne ryzyko. Serwis nie ponosi odpowiedzialności za ewentualne straty majątkowe.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">4. Prawa autorskie</h2>
            <p>Wszelkie treści, struktura układu oraz kod serwisu są chronione prawem autorskim. Kopiowanie i rozpowszechnianie analiz generowanych przez naszą sztuczną inteligencję bez wyraźnej zgody administracji jest zabronione.</p>
          </section>
        </div>
        
        <div className="mt-8 text-center">
          <Link href="/" className="text-emerald-400 font-bold hover:text-emerald-300 transition-colors">
            &larr; Wróć do strony głównej
          </Link>
        </div>
      </div>
    </main>
  );
}
