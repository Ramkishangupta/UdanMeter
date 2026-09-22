import React, { useState } from 'react';
import { Gauge, Search, ArrowRight, ShieldCheck, Filter } from 'lucide-react';

export default function DynamicHeatmap({ heatmapData }) {
  const [searchTerm, setSearchTerm] = useState('');

  const defaultData = [
    { origin: 'DEL', destination: 'BOM', route_name: 'Delhi - Mumbai', weight: 0.18, avg_fare: 4850, min_fare: 3600, max_fare: 8900, t1_fare: 8400, t45_fare: 3600, pressure_index: 1.08 },
    { origin: 'DEL', destination: 'BLR', route_name: 'Delhi - Bengaluru', weight: 0.14, avg_fare: 5400, min_fare: 4200, max_fare: 9800, t1_fare: 9500, t45_fare: 4100, pressure_index: 1.20 },
    { origin: 'BOM', destination: 'BLR', route_name: 'Mumbai - Bengaluru', weight: 0.12, avg_fare: 3650, min_fare: 2800, max_fare: 6500, t1_fare: 6200, t45_fare: 2800, pressure_index: 0.81 },
    { origin: 'DEL', destination: 'CCU', route_name: 'Delhi - Kolkata', weight: 0.09, avg_fare: 4450, min_fare: 3400, max_fare: 7900, t1_fare: 7600, t45_fare: 3300, pressure_index: 0.99 },
    { origin: 'BLR', destination: 'HYD', route_name: 'Bengaluru - Hyderabad', weight: 0.08, avg_fare: 2950, min_fare: 2200, max_fare: 5200, t1_fare: 5000, t45_fare: 2150, pressure_index: 0.66 },
    { origin: 'MAA', destination: 'DEL', route_name: 'Chennai - Delhi', weight: 0.08, avg_fare: 5250, min_fare: 4100, max_fare: 9400, t1_fare: 9100, t45_fare: 4050, pressure_index: 1.17 },
    { origin: 'CCU', destination: 'BLR', route_name: 'Kolkata - Bengaluru', weight: 0.07, avg_fare: 4900, min_fare: 3800, max_fare: 8600, t1_fare: 8300, t45_fare: 3750, pressure_index: 1.09 },
    { origin: 'DEL', destination: 'HYD', route_name: 'Delhi - Hyderabad', weight: 0.07, avg_fare: 4200, min_fare: 3300, max_fare: 7500, t1_fare: 7200, t45_fare: 3250, pressure_index: 0.93 },
    { origin: 'BOM', destination: 'GOI', route_name: 'Mumbai - Goa', weight: 0.06, avg_fare: 2850, min_fare: 2100, max_fare: 5400, t1_fare: 5100, t45_fare: 2050, pressure_index: 0.63 },
    { origin: 'BLR', destination: 'MAA', route_name: 'Bengaluru - Chennai', weight: 0.04, avg_fare: 2350, min_fare: 1800, max_fare: 4300, t1_fare: 4100, t45_fare: 1750, pressure_index: 0.52 },
    { origin: 'DEL', destination: 'PNQ', route_name: 'Delhi - Pune', weight: 0.04, avg_fare: 4500, min_fare: 3500, max_fare: 8100, t1_fare: 7800, t45_fare: 3450, pressure_index: 1.00 },
    { origin: 'BOM', destination: 'AMD', route_name: 'Mumbai - Ahmedabad', weight: 0.03, avg_fare: 2600, min_fare: 2000, max_fare: 4800, t1_fare: 4600, t45_fare: 1950, pressure_index: 0.58 }
  ];

  const data = (heatmapData && heatmapData.length > 0) ? heatmapData : defaultData;

  const filteredData = data.filter(item =>
    item.route_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.origin.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.destination.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="glass-panel p-6 mb-6 shadow-2xl border border-slate-800">
      
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between pb-4 mb-6 border-b border-slate-800 gap-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Gauge className="w-5 h-5 text-emerald-400" />
            Inter-City Domestic Route Fare Matrix & Route Pressure Index
          </h2>
          <p className="text-xs text-slate-400">
            DGCA passenger traffic-weighted city pairs, comparing mean ticket fares, T+1 surge fares, and T+45 advance discount fares
          </p>
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search route or airport (DEL, BOM)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>
      </div>

      {/* Heatmap Table */}
      <div className="overflow-x-auto rounded-xl border border-slate-800/80">
        <table className="w-full text-left text-xs">
          <thead>
            <tr className="bg-slate-900/90 text-slate-400 uppercase tracking-wider border-b border-slate-800">
              <th className="py-3.5 px-4 font-bold">Route / City Pair</th>
              <th className="py-3.5 px-4 text-center font-bold">DGCA Traffic Weight</th>
              <th className="py-3.5 px-4 text-right font-bold">Average Fare</th>
              <th className="py-3.5 px-4 text-right font-bold">Min Fare</th>
              <th className="py-3.5 px-4 text-right font-bold">Max Fare</th>
              <th className="py-3.5 px-4 text-right font-bold">T+1 Surge</th>
              <th className="py-3.5 px-4 text-right font-bold">T+45 Early Bird</th>
              <th className="py-3.5 px-4 text-center font-bold">Pressure Index</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 bg-slate-950/40">
            {filteredData.map((item, idx) => {
              const isHighPressure = item.pressure_index > 1.10;
              const isLowPressure = item.pressure_index < 0.85;

              return (
                <tr key={idx} className="hover:bg-slate-800/50 transition-colors">
                  <td className="py-3.5 px-4 font-semibold text-white flex items-center gap-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${
                      isHighPressure ? 'bg-rose-500 shadow-sm shadow-rose-500' : isLowPressure ? 'bg-emerald-400 shadow-sm shadow-emerald-400' : 'bg-sky-400'
                    }`}></span>
                    <span>{item.route_name}</span>
                    <span className="text-[10px] font-mono text-slate-400 px-1.5 py-0.5 rounded bg-slate-800">({item.origin}-{item.destination})</span>
                  </td>
                  <td className="py-3.5 px-4 text-center font-mono text-slate-300">
                    {(item.weight * 100).toFixed(1)}%
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono font-bold text-white">
                    ₹{item.avg_fare?.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-emerald-400 font-semibold">
                    ₹{item.min_fare?.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-rose-400 font-semibold">
                    ₹{item.max_fare?.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-amber-400 font-semibold">
                    ₹{item.t1_fare?.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 text-right font-mono text-sky-300 font-semibold">
                    ₹{item.t45_fare?.toLocaleString()}
                  </td>
                  <td className="py-3.5 px-4 text-center">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-bold font-mono ${
                      isHighPressure
                        ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        : isLowPressure
                        ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                        : 'bg-sky-500/10 text-sky-400 border border-sky-500/20'
                    }`}>
                      {item.pressure_index?.toFixed(2)}x
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
