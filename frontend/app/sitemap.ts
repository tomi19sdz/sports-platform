import { MetadataRoute } from 'next';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // UWAGA: Upewnij się, czy w ustawieniach Vercel główną domeną jest wersja z "www" czy bez!
  // Jeśli masz włączone www, zmień poniższy link na 'https://www.sportsplatform.pl'
  const baseUrl = 'https://sportsplatform.pl';

  // 1. Podstrony statyczne (w tym nowe strony wygenerowane dla AdSense)
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: `${baseUrl}`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/history`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/live-sport`,
      lastModified: new Date(),
      changeFrequency: 'hourly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/polityka-prywatnosci`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/kontakt`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
  ];

  // 2. Dynamiczne podstrony meczów
  let dynamicRoutes: MetadataRoute.Sitemap = [];
  
  try {
    const res = await fetch('https://tomi19sdz.pythonanywhere.com/api/matches/', {
      next: { revalidate: 3600 } // Odświeża cache sitemapy co godzinę
    });
    
    if (res.ok) {
      const groupedMatches = await res.json();
      
      // Spłaszczamy obiekt, aby wyciągnąć wszystkie mecze do jednej tablicy
      const allMatches = Object.values(groupedMatches).flat() as any[];
      
      dynamicRoutes = allMatches.map((match) => ({
        url: `${baseUrl}/match/${match.id}`,
        lastModified: new Date(match.match_date),
        changeFrequency: 'daily',
        priority: 0.7,
      }));
    }
  } catch (error) {
    console.error("Błąd pobierania meczów do mapy witryny:", error);
  }

  // Zwracamy połączoną mapę: statyczne + dynamiczne
  return [...staticRoutes, ...dynamicRoutes];
}