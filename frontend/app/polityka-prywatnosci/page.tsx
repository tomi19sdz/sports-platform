import React from 'react';

export default function PrivacyPolicyPage() {
  return (
    <main className="min-h-screen bg-[#0a0f16] text-slate-200 p-8">
      <div className="max-w-4xl mx-auto mt-10">
        <h1 className="text-4xl font-black text-white mb-8">Polityka Prywatności</h1>
        
        <div className="space-y-6 text-slate-400 leading-relaxed bg-slate-900/40 p-8 rounded-2xl border border-slate-800/80">
          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">1. Informacje ogólne</h2>
            <p>Niniejsza Polityka Prywatności określa zasady przetwarzania i ochrony danych osobowych przekazanych przez Użytkowników w związku z korzystaniem z platformy Sports Platform.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">2. Pliki cookies i reklamy Google AdSense</h2>
            <ul className="list-disc pl-5 space-y-2">
              <li>Na naszej stronie wyświetlane są reklamy dostarczane przez zewnętrzne firmy reklamowe, w tym Google.</li>
              <li>Google, jako dostawca zewnętrzny, wykorzystuje pliki cookie do wyświetlania reklam w tej witrynie.</li>
              <li>Dzięki plikom cookie DART firma Google może wyświetlać użytkownikom spersonalizowane reklamy na podstawie ich wizyt na naszej oraz innych stronach internetowych.</li>
              <li>Użytkownicy mogą zrezygnować z używania plików cookie DART. W tym celu należy odwiedzić stronę <a href="https://policies.google.com/technologies/ads" className="text-emerald-400 hover:underline" target="_blank" rel="noreferrer">polityki prywatności reklam Google</a>.</li>
            </ul>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">3. Gromadzenie i wykorzystywanie danych</h2>
            <p>Serwis automatycznie zbiera standardowe dane analityczne, takie jak adres IP, typ przeglądarki, czas wizyty oraz odwiedzane strony. Dane te służą wyłącznie do celów statystycznych, poprawy jakości naszych analiz i prawidłowego działania witryny.</p>
          </section>

          <section>
            <h2 className="text-xl font-bold text-slate-200 mb-3">4. Kontakt</h2>
            <p>W razie pytań dotyczących polityki prywatności prosimy o kontakt poprzez zakładkę Kontakt dostępną w naszym serwisie.</p>
          </section>
        </div>
      </div>
    </main>
  );
}