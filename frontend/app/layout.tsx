import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Footer from "@/components/Footer";
import Navbar from "@/components/Navbar"; // <-- Twój poprawny import

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Sports Platform",
  description: "Nadchodzące spotkania, wyniki na żywo i analizy",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pl">
      <head>
        {/* Tag weryfikacyjny Google AdSense (Metatag) */}
        <meta name="google-adsense-account" content="ca-pub-1288941577582966" />
        <meta name="google-site-verification" content="Iirk2-1OjlnJnrmnWfhe9_HLPR1_cbpXh7J0qXanIBw" />
        {/* Skrypt pobierający reklamy AdSense */}
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1288941577582966" crossOrigin="anonymous"></script>
      </head>
      <body className={`${inter.className} flex flex-col min-h-screen`}>
        
        {/* TUTAJ WSTAWIAMY NAVBAR - na samej górze strony przed resztą treści */}
        <Navbar />
        
        <div className="flex-grow">
          {children}
        </div>
        
        <Footer />
      </body>
    </html>
  );
}