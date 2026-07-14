import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

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
        {/* DOKŁADNIE TWÓJ KOD ADSENSE */}
        <script 
          async 
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1288941577582966" 
          crossOrigin="anonymous"
        ></script>
      </head>
      <body className={inter.className}>{children}</body>
    </html>
  );
}