import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Layers, DollarSign } from 'lucide-react';

export default function FareDecomposition() {
  const data = [
    { name: 'Base Ticket Fare', value: 64.5, color: '#38bdf8' },
    { name: 'Fuel Surcharge (YQ)', value: 21.0, color: '#8b5cf6' },
    { name: 'Statutory Airport Taxes (UDF/PSF)', value: 10.5, color: '#f59e0b' },
    { name: 'Convenience / Gateway Fees', value: 4.0, color: '#10b981' }
  ];

  return (
    <div className="glass-panel p-6 mb-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 mb-4 border-b border-slate-800 gap-2">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-sky-400" />
            Airfare Component Decomposition Architecture
          </h2>
          <p className="text-xs text-slate-400">
            Decomposing gross retail quotes into pure transportation fare, statutory airport development fees, and OTA charges
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        
        {/* Pie Chart */}
        <div className="h-[260px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={95}
                paddingAngle={4}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} stroke="#0f172a" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip
                formatter={(val) => [`${val}%`, 'Share of Total Fare']}
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', color: '#f8fafc', fontSize: '12px' }}
              />
              <Legend verticalAlign="bottom" height={36} iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Structural Breakdown List */}
        <div className="space-y-3">
          {data.map((item, idx) => (
            <div key={idx} className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="w-3.5 h-3.5 rounded-full flex-shrink-0" style={{ backgroundColor: item.color }}></span>
                <div>
                  <span className="text-xs font-bold text-white">{item.name}</span>
                  <p className="text-[11px] text-slate-400">MoSPI Inflation Decomposition Sub-Basket</p>
                </div>
              </div>
              <span className="text-sm font-extrabold text-white font-mono">{item.value}%</span>
            </div>
          ))}
        </div>

      </div>
    </div>
  );
}
