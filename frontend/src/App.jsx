import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import IndexTicker from './components/IndexTicker';
import ApixChart from './components/ApixChart';
import DynamicHeatmap from './components/DynamicHeatmap';
import ElasticityChart from './components/ElasticityChart';
import FareDecomposition from './components/FareDecomposition';
import CarrierParity from './components/CarrierParity';
import BacktestingSuite from './components/BacktestingSuite';
import ApiPortal from './components/ApiPortal';

const API_BASE = 'http://127.0.0.1:8000/api/v1';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [heatmap, setHeatmap] = useState([]);
  const [elasticity, setElasticity] = useState([]);
  const [parity, setParity] = useState([]);
  const [backtest, setBacktest] = useState(null);
  const [isScraping, setIsScraping] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      const [sumRes, histRes, heatRes, elastRes, parRes, backRes] = await Promise.all([
        axios.get(`${API_BASE}/apix/summary`),
        axios.get(`${API_BASE}/apix/history?days=30`),
        axios.get(`${API_BASE}/heatmap`),
        axios.get(`${API_BASE}/elasticity`),
        axios.get(`${API_BASE}/parity`),
        axios.get(`${API_BASE}/backtest`)
      ]);

      if (sumRes.data) setSummary(sumRes.data);
      if (histRes.data) setHistory(histRes.data);
      if (heatRes.data) setHeatmap(heatRes.data);
      if (elastRes.data) setElasticity(elastRes.data);
      if (parRes.data) setParity(parRes.data);
      if (backRes.data) setBacktest(backRes.data);
    } catch (err) {
      console.warn('Backend API endpoint warning, using resilient fallback state:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const handleTriggerScrape = async () => {
    try {
      setIsScraping(true);
      await axios.post(`${API_BASE}/scrape/trigger`);
      await fetchAllData();
    } catch (err) {
      console.error('Scrape error:', err);
    } finally {
      setIsScraping(false);
    }
  };

  const handleExportCsv = () => {
    window.open(`${API_BASE}/export/csv`, '_blank');
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 font-sans pb-12 selection:bg-sky-500 selection:text-white">
      
      {/* Navbar Header */}
      <Navbar
        onTriggerScrape={handleTriggerScrape}
        isScraping={isScraping}
        onExportCsv={handleExportCsv}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-8">
        
        {/* Real-time National Index Metric Ticker (Always Visible) */}
        <IndexTicker summary={summary} />

        {/* Tab Views */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <ApixChart history={history} />
            <FareDecomposition />
            <CarrierParity parityData={parity} />
            <DynamicHeatmap heatmapData={heatmap} />
          </div>
        )}

        {activeTab === 'heatmap' && (
          <DynamicHeatmap heatmapData={heatmap} />
        )}

        {activeTab === 'elasticity' && (
          <ElasticityChart elasticityData={elasticity} />
        )}

        {activeTab === 'parity' && (
          <CarrierParity parityData={parity} />
        )}

        {activeTab === 'backtest' && (
          <BacktestingSuite backtestData={backtest} />
        )}

        {activeTab === 'api' && (
          <ApiPortal onExportCsv={handleExportCsv} />
        )}

      </main>

      {/* Footer */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-8 mt-12 pt-6 border-t border-slate-800/80 text-center text-xs text-slate-500 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div>
          © 2026 National Statistical Office (NSO), MoSPI & Reserve Bank of India (RBI) • SIH Problem Statement 26056
        </div>
        <div className="flex items-center gap-4 text-slate-400 font-medium">
          <span>Automated Ethical Web Scraping</span>
          <span>•</span>
          <span>Fisher Price Index</span>
          <span>•</span>
          <span>DGCA Benchmarked</span>
        </div>
      </footer>

    </div>
  );
}
