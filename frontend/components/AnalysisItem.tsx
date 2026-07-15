'use client';
import React, { useState } from 'react';

export default function AnalysisItem({ text }: { text: string }) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!text) return null;

  const lines = text.split('\n');
  const isLong = lines.length > 10;

  const displayText = (!isExpanded && isLong)
    ? lines.slice(0, 10).join('\n') + '\n...'
    : text;

  return (
    <div className="bg-[#111827] border border-slate-700/60 p-6 rounded-2xl shadow-lg transition-all duration-300">
      <div className="text-slate-300 whitespace-pre-wrap leading-relaxed text-sm md:text-base">
        {displayText}
      </div>

      {isLong && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="mt-5 text-emerald-500 hover:text-emerald-400 font-bold transition-colors flex items-center gap-2 px-4 py-2 bg-emerald-500/10 hover:bg-emerald-500/20 rounded-xl w-fit"
        >
          {isExpanded ? '↑ Zwiń analizę' : '↓ Czytaj dalej...'}
        </button>
      )}
    </div>
  );
}