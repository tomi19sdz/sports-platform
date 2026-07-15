import React from 'react';

export default function Footer() {
  return (
    <footer className="bg-slate-950 border-t border-slate-900 py-10 mt-auto">
      <div className="max-w-4xl mx-auto px-8 text-center text-slate-500 text-sm">
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