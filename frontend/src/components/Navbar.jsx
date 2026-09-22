import React from 'react';
import { Plane, LayoutDashboard, MapPin, TrendingDown, Scale, Award, Code2, RefreshCw, Download } from 'lucide-react';

export default function Navbar({ onTriggerScrape, isScraping, onExportCsv, activeTab, setActiveTab }) {
  const tabs = [
    { id: 'overview', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'heatmap', label: 'Route Heatmap', icon: MapPin },
    { id: 'elasticity', label: 'Lead Elasticity', icon: TrendingDown },
    { id: 'parity', label: 'Carrier Parity', icon: Scale },
    { id: 'backtest', label: 'DGCA Backtest', icon: Award },
    { id: 'api', label: 'API & Export', icon: Code2 }
  ];

  return (
    <header className="sticky top-0 z-50 bg-slate-950/95 backdrop-blur-2xl border-b border-slate-800/80 px-4 sm:px-8 py-3 mb-6 shadow-2xl">
      <div className="max-w-7xl mx-auto space-y-3">
        
        {/* Tier 1: Branding Header (Left) + Status & Actions (Right) */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-1 border-b border-slate-900">
          
          {/* Logo & MoSPI / RBI Credentials */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-500 via-blue-600 to-indigo-600 p-0.5 flex items-center justify-center shadow-lg shadow-sky-500/25 shrink-0">
              <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                <Plane className="w-4 h-4 text-sky-400 transform -rotate-45" />
              </div>
            </div>

            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base sm:text-lg font-extrabold tracking-tight text-white">
                  MoSPI Airfare Price Index
                </h1>
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-sky-500/15 text-sky-400 border border-sky-500/30">
                  APIx v1.0
                </span>
                <span className="hidden md:inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 ml-2">
                  <span className="live-dot"></span> Real-time Live Feed
                </span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium">
                National Statistical Office (NSO) • Ministry of Statistics & Programme Implementation | RBI
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2.5 self-end sm:self-auto">
            <button
              onClick={onTriggerScrape}
              disabled={isScraping}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-400 text-xs font-bold border border-slate-800 hover:border-sky-500/40 transition-all shadow-md disabled:opacity-50"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isScraping ? 'animate-spin' : ''}`} />
              <span>{isScraping ? 'Scraping...' : 'Trigger Scrape'}</span>
            </button>

            <button
              onClick={onExportCsv}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/25 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>CSV Export</span>
            </button>
          </div>

        </div>

        {/* Tier 2: 6 Evenly-Spaced Navigation Tabs (Zero Scrollbar) */}
        <nav className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 bg-slate-900/80 p-1.5 rounded-2xl border border-slate-800/80 shadow-inner">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;

            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-sky-500 via-blue-600 to-indigo-600 text-white shadow-lg shadow-sky-500/25 scale-[1.02]'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

      </div>
    </header>
  );
}
