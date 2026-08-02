'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav className="w-full bg-[#0a0f16] border-b border-slate-800/80 p-4 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* LOGO / KLIKALNY NAPIS */}
        <Link 
          href="/" 
          className="flex items-center space-x-2 text-2xl md:text-3xl font-black tracking-tight hover:opacity-80 transition-opacity"
        >
          <span className="text-white">Sports</span>
          <span className="text-[#00a859]">Platform</span>
        </Link>

        {/* ZAKŁADKI / PRZYCISKI */}
        <div className="flex flex-wrap justify-center gap-2 sm:gap-4">
          <Link 
            href="/" 
            className={`px-4 sm:px-6 py-2 rounded-full font-bold transition-all duration-300 text-sm sm:text-base ${
              pathname === '/' 
                ? 'bg-[#00a859] text-white shadow-lg shadow-[#00a859]/20' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
            }`}
          >
            Nadchodzące
          </Link>
          
          <Link 
            href="/history" 
            className={`px-4 sm:px-6 py-2 rounded-full font-bold transition-all duration-300 text-sm sm:text-base ${
              pathname === '/history' 
                ? 'bg-slate-600 text-white shadow-lg' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
            }`}
          >
            Historia
          </Link>
          
          <Link 
            href="/live" 
            className={`px-4 sm:px-6 py-2 rounded-full font-bold transition-all duration-300 text-sm sm:text-base ${
              pathname === '/live' 
                ? 'bg-red-600 text-white shadow-lg shadow-red-500/20' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
            }`}
          >
            Live Sport
          </Link>
          
          <Link 
            href="/news" 
            className={`px-4 sm:px-6 py-2 rounded-full font-bold transition-all duration-300 text-sm sm:text-base ${
              pathname === '/news' 
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/20' 
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
            }`}
          >
            Wiadomości
          </Link>
        </div>

      </div>
    </nav>
  );
}