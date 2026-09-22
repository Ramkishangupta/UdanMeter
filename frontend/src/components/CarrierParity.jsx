import React from 'react';
import { Scale, ArrowUpRight, ShieldCheck, Building2 } from 'lucide-react';

export default function CarrierParity({ parityData }) {
  const defaultData = [
    { carrier: 'IndiGo', direct_avg_fare: 4850, ota_avg_fare: 5180, ota_markup_pct: 6.8, total_quotes: 142 },
    { carrier: 'Air India', direct_avg_fare: 5450, ota_avg_fare: 5790, ota_markup_pct: 6.2, total_quotes: 118 },
    { carrier: 'Air India Express', direct_avg_fare: 4600, ota_avg_fare: 4910, ota_markup_pct: 6.7, total_quotes: 98 },
    { carrier: 'Akasa Air', direct_avg_fare: 4500, ota_avg_fare: 4810, ota_markup_pct: 6.9, total_quotes: 86 },
    { carrier: 'SpiceJet', direct_avg_fare: 4700, ota_avg_fare: 5020, ota_markup_pct: 6.8, total_quotes: 92 }
  ];

  const data = (parityData && parityData.length > 0) ? parityData : defaultData;

  return (
    <div className="glass-panel p-6 mb-6 shadow-2xl border border-slate-800">
      
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 mb-5 border-b border-slate-800 gap-2">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Scale className="w-5 h-5 text-amber-400" />
            Airline Direct Portal vs OTA Price Parity & Markup Audit
          </h2>
          <p className="text-xs text-slate-400">
            Auditing price quotes across IndiGo, Air India, Air India Express, Akasa Air, SpiceJet vs MakeMyTrip, Yatra, EaseMyTrip, Cleartrip & Ixigo
          </p>
        </div>
      </div>

      {/* Grid Layout - Responsive columns with clean spacing */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-4">
        {data.map((item, idx) => (
          <div key={idx} className="glass-card p-4 flex flex-col justify-between border border-slate-800 hover:border-amber-500/40 transition-all shadow-lg min-w-0">
            
            {/* Header: Carrier Name & Quotes Badge */}
            <div>
              <div className="flex items-center justify-between gap-2 mb-3 pb-2.5 border-b border-slate-800/80">
                <span className="text-sm font-extrabold text-white truncate">{item.carrier}</span>
                <span className="text-[10px] text-sky-400 font-mono font-semibold bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/20 shrink-0">
                  {item.total_quotes} Quotes
                </span>
              </div>

              {/* Pricing Breakdown */}
              <div className="space-y-2.5 my-3 text-xs">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-slate-400 text-[11px]">Direct Airline:</span>
                  <span className="font-mono font-extrabold text-white">₹{item.direct_avg_fare?.toLocaleString()}</span>
                </div>
                <div className="flex items-center justify-between gap-2">
                  <span className="text-slate-400 text-[11px]">OTA Aggregate:</span>
                  <span className="font-mono font-extrabold text-amber-400">₹{item.ota_avg_fare?.toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* Footer: OTA Convenience Markup Badge */}
            <div className="pt-2.5 border-t border-slate-800/80 flex items-center justify-between gap-2 text-xs">
              <span className="text-slate-400 text-[10px] uppercase font-semibold">OTA Markup:</span>
              <span className="font-mono font-extrabold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded border border-emerald-500/20 text-[11px]">
                +{item.ota_markup_pct?.toFixed(1)}%
              </span>
            </div>

          </div>
        ))}
      </div>
    </div>
  );
}
