import Link from 'next/link';
import React from 'react';

// Odświeżamy stronę co 1 godzinę (3600 sekund), aby nie spamować serwerów sportowych,
// a jednocześnie mieć zawsze w miarę świeże informacje.
export const revalidate = 3600;

interface NewsItem {
  title: string;
  pubDate: string;
  link: string;
  thumbnail: string;
  description: string;
}

async function getSportsNews(): Promise<NewsItem[]> {
  // Jako przykład pobieramy darmowy kanał RSS z polskimi wiadomościami (Piłka Nożna)
  // Używamy darmowego rss2json, aby łatwo odczytać to w Next.js
  const rssUrl = 'https://sportowefakty.wp.pl/pilka-nozna/rss.xml';
  const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`;
  
  try {
    const res = await fetch(apiUrl, { next: { revalidate: 3600 } });
    if (!res.ok) return [];
    
    const data = await res.json();
    return data.items || [];
  } catch (error) {
    console.error("Błąd podczas pobierania wiadomości:", error);
    return [];
  }
}

export default async function NewsPage() {
  const news = await getSportsNews();

  // Funkcja czyszcząca tagi HTML z opisu (czasem przychodzą z RSS)
  const stripHtml = (html: string) => html.replace(/<[^>]+>/g, '');

  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 text-center mt-10">
          <h1 className="text-5xl font-black text-white mb-4 tracking-tight">
            Sports <span className="text-blue-500">News</span>
          </h1>
          <p className="text-slate-400 text-lg mb-8">
            Najświeższe wiadomości ze świata piłki nożnej. Aktualizowane automatycznie.
          </p>
          
          {/* Menu Nawigacyjne */}
          <div className="flex justify-center space-x-4">
            <Link href="/" className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full font-bold hover:bg-slate-700 transition-colors">
              Nadchodzące
            </Link>
            <Link href="/history" className="px-6 py-2 bg-slate-800 text-slate-300 rounded-full font-bold hover:bg-slate-700 transition-colors">
              Historia
            </Link>
            <Link href="/news" className="px-6 py-2 bg-blue-600 text-white rounded-full font-bold shadow-lg shadow-blue-500/20">
              Wiadomości
            </Link>
          </div>
        </header>

        {news.length === 0 ? (
          <div className="text-center text-slate-500 mt-20 flex flex-col items-center">
            <span className="text-6xl mb-4">📰</span>
            <p className="text-xl">Chwilowy brak wiadomości do wyświetlenia.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {news.map((item, index) => (
              <a 
                key={index} 
                href={item.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="group bg-slate-900/50 border border-slate-800 rounded-2xl overflow-hidden hover:border-blue-500/50 transition-all duration-300 flex flex-col shadow-lg shadow-slate-950 hover:shadow-blue-900/20"
              >
                {/* Zdjęcie z artykułu (jeśli jest), w przeciwnym razie ładny gradient */}
                <div className="h-48 w-full bg-slate-800 relative overflow-hidden">
                  {item.thumbnail ? (
                    <img 
                      src={item.thumbnail} 
                      alt={item.title} 
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-slate-800 to-slate-900 flex items-center justify-center">
                      <span className="text-4xl">⚽</span>
                    </div>
                  )}
                  {/* Data publikacji unosząca się na zdjęciu */}
                  <div className="absolute bottom-3 left-3 bg-black/70 backdrop-blur-sm px-3 py-1 rounded-lg text-xs font-bold text-slate-300 border border-white/10">
                    {new Date(item.pubDate).toLocaleString('pl-PL', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                
                {/* Treść karty */}
                <div className="p-6 flex flex-col flex-grow">
                  <h2 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors line-clamp-2">
                    {item.title}
                  </h2>
                  <p className="text-sm text-slate-400 line-clamp-3 mb-4 flex-grow">
                    {stripHtml(item.description)}
                  </p>
                  
                  <div className="mt-auto flex items-center text-blue-500 text-sm font-bold group-hover:text-blue-400 transition-colors">
                    Czytaj dalej na portalu <span className="ml-2">→</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}