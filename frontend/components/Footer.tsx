import React from 'react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 py-10 mt-auto">
      <div className="max-w-4xl mx-auto px-8 text-center text-slate-500 text-sm">
        
        {/* --- DODANE LINKI DLA GOOGLE ADSENSE --- */}
        <div className="flex justify-center space-x-6 mb-6">
          <Link href="/polityka-prywatnosci" className="hover:text-emerald-400 transition-colors font-medium">
            Polityka Prywatności
          </Link>
          <Link href="/kontakt" className="hover:text-emerald-400 transition-colors font-medium">
            Kontakt
          </Link>
        </div>
        {/* --------------------------------------- */}

        <p className="mb-3 text-slate-400 font-bold">
          © {new Date().getFullYear()} Sports Platform. Wszelkie prawa zastrzeżone.
        </p>
        <p className="max-w-2xl mx-auto leading-relaxed text-xs md:text-sm">
          Serwis ma charakter wyłącznie informacyjny. Nie prowadzimy działalności hazardowej 
          ani nie przyjmujemy zakładów bukmacherskich. Treści prezentowane na stronie 
          służą wyłącznie celom statystycznym i rozrywkowym.
        </p>
      </div>
    </footer>
  );
}