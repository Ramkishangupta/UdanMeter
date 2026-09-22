import React from 'react';
import { TrendingUp, TrendingDown, Layers, Database, BarChart3, Activity } from 'lucide-react';

export default function IndexTicker({ summary }) {
  const data = summary || {
    apix_national: 104.85,
    laspeyres_index: 105.20,
    paasche_index: 104.50,
    jevons_index: 104.75,
    cpi_transport_benchmark: 101.40,
    pct_change_daily: 0.85,
    active_basket_quotes: 583
  };

  const isPositive = data.pct_change_daily >= 0;

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      
      {/* 1. National APIx Index (Fisher Ideal) */}
      <div className="glass-card p-5 relative overflow-hidden border-l-4 border-l-sky-500 shadow-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            APIx National Index (Fisher)
          </span>
          <div className="p-2 rounded-lg bg-sky-500/10 text-sky-400">
            <Activity className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-3xl font-extrabold text-white font-mono tracking-tight">
            {data.apix_national?.toFixed(2)}
          </span>
          <span className={`inline-flex items-center text-xs font-bold px-2.5 py-0.5 rounded-full ${
            isPositive ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
          }`}>
            {isPositive ? <TrendingUp className="w-3 h-3 mr-1" /> : <TrendingDown className="w-3 h-3 mr-1" />}
            {data.pct_change_daily > 0 ? '+' : ''}{data.pct_change_daily?.toFixed(2)}%
          </span>
        </div>
        <p className="text-[11px] text-slate-400 mt-2.5 flex items-center justify-between">
          <span>Fisher Ideal Aggregation</span>
          <span className="text-sky-400 font-mono font-bold">Base = 100.0</span>
        </p>
      </div>

      {/* 2. Laspeyres vs Paasche Spread */}
      <div className="glass-card p-5 relative overflow-hidden border-l-4 border-l-purple-500 shadow-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            Laspeyres / Paasche Spread
          </span>
          <div className="p-2 rounded-lg bg-purple-500/10 text-purple-400">
            <Layers className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline justify-between">
          <div>
            <span className="text-[11px] text-slate-400">Laspeyres ($L_t$): </span>
            <span className="text-lg font-bold text-purple-300 font-mono">{data.laspeyres_index?.toFixed(1)}</span>
          </div>
          <div className="text-right">
            <span className="text-[11px] text-slate-400">Paasche ($P_t$): </span>
            <span className="text-lg font-bold text-emerald-400 font-mono">{data.paasche_index?.toFixed(1)}</span>
          </div>
        </div>
        <div className="w-full bg-slate-800/80 h-1.5 rounded-full mt-3 overflow-hidden">
          <div className="bg-gradient-to-r from-purple-500 to-sky-400 h-full rounded-full" style={{ width: '68%' }}></div>
        </div>
        <p className="text-[11px] text-slate-400 mt-2 flex items-center justify-between">
          <span>Jevons Elementary:</span>
          <span className="text-purple-300 font-mono font-bold">{data.jevons_index?.toFixed(1)}</span>
        </p>
      </div>

      {/* 3. Basket Coverage & Active Quotes */}
      <div className="glass-card p-5 relative overflow-hidden border-l-4 border-l-emerald-500 shadow-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            Scraped Basket Coverage
          </span>
          <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400">
            <Database className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-2">
          <span className="text-3xl font-extrabold text-white font-mono tracking-tight">
            {data.active_basket_quotes}
          </span>
          <span className="text-xs text-emerald-400 font-bold px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">
            Active Quotes
          </span>
        </div>
        <p className="text-[11px] text-slate-400 mt-2.5">
          12 DGCA City Pairs • 5 Lead Windows ($T+1 \dots T+45$)
        </p>
      </div>

      {/* 4. Standard CPI Transport Benchmark */}
      <div className="glass-card p-5 relative overflow-hidden border-l-4 border-l-amber-500 shadow-xl">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
            Standard CPI Transport Index
          </span>
          <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400">
            <BarChart3 className="w-4 h-4" />
          </div>
        </div>
        <div className="flex items-baseline gap-3">
          <span className="text-3xl font-extrabold text-amber-400 font-mono tracking-tight">
            {data.cpi_transport_benchmark?.toFixed(2)}
          </span>
          <span className="text-xs text-slate-400 font-medium">NSO Baseline</span>
        </div>
        <p className="text-[11px] text-amber-300/90 mt-2.5 flex items-center justify-between">
          <span>APIx Lead Margin:</span>
          <span className="font-bold font-mono text-amber-400">
            +{(data.apix_national - data.cpi_transport_benchmark).toFixed(2)} pts
          </span>
        </p>
      </div>

    </div>
  );
}
