import { useEffect, useState } from 'react';
import { Activity, CloudRain, Gauge, MapPin, RefreshCw, TrainFront, TriangleAlert } from 'lucide-react';

const API = 'http://localhost:8000';

function formatEta(value) {
  return new Date(value).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export default function RailCastApp() {
  const [trains, setTrains] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadTrains() {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/trains`);
      if (!response.ok) throw new Error('Unable to fetch live train data');
      const data = await response.json();
      setTrains(data);
      setSelected((current) => data.find((item) => item.train.id === current?.train.id) || data[0]);
      setError('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadTrains();
    const timer = setInterval(loadTrains, 30000);
    return () => clearInterval(timer);
  }, []);

  const delayed = trains.filter((item) => item.train.delay_minutes > 15).length;
  const averageConfidence = trains.length ? Math.round(trains.reduce((sum, item) => sum + item.train.confidence, 0) / trains.length) : 0;

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand"><TrainFront size={25} /><span>RAIL<span className="brand-accent">/</span>CAST</span></div>
        <div className="live-status"><span className="pulse" /> Live operations view <button className="icon-button" onClick={loadTrains} title="Refresh data"><RefreshCw size={16} /></button></div>
      </header>

      <section className="hero">
        <div><p className="eyebrow">SMART AUTOMATION / 26 028</p><h1>Arrival intelligence<br /><em>for every mile.</em></h1><p className="hero-copy">Dynamic ETA forecasts for coaching trains, continuously tuned to conditions on the ground.</p></div>
        <div className="hero-stamp"><span>LAST SYNC</span><strong>{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</strong><small>Auto-refresh · 30 sec</small></div>
      </section>

      <section className="metric-grid">
        <div className="metric"><span className="metric-label"><Activity size={15} /> TRACKED TRAINS</span><strong>{trains.length || '—'}</strong><small>Across active corridors</small></div>
        <div className="metric warning"><span className="metric-label"><TriangleAlert size={15} /> NEED ATTENTION</span><strong>{delayed || '—'}</strong><small>More than 15 min behind</small></div>
        <div className="metric"><span className="metric-label"><Gauge size={15} /> MODEL CONFIDENCE</span><strong>{averageConfidence ? `${averageConfidence}%` : '—'}</strong><small>Based on live signal quality</small></div>
      </section>

      <section className="content-grid">
        <div className="panel train-panel"><div className="panel-heading"><div><p className="eyebrow">NETWORK PULSE</p><h2>Active services</h2></div><span className="count-badge">{trains.length} trains</span></div>
          {loading && <p className="empty">Loading live forecast...</p>}
          {error && <p className="error">{error}. Start the FastAPI server on port 8000.</p>}
          <div className="train-list">{trains.map((item) => <button className={`train-row ${selected?.train.id === item.train.id ? 'selected' : ''}`} key={item.train.id} onClick={() => setSelected(item)}>
            <div className="train-icon"><TrainFront size={18} /></div><div className="train-info"><strong>{item.train.number} · {item.train.name}</strong><span>{item.train.current_station} <span className="arrow">→</span> {item.train.next_station}</span></div><div className="train-eta"><strong>{formatEta(item.eta)}</strong><span className={item.train.delay_minutes > 15 ? 'late' : 'on-time'}>{item.train.delay_minutes > 15 ? `+${item.train.delay_minutes} min` : 'On time'}</span></div>
          </button>)}</div>
        </div>

        <div className="panel detail-panel">{selected ? <><div className="panel-heading"><div><p className="eyebrow">FORECAST DETAIL</p><h2>{selected.train.number}</h2></div><span className="confidence">{selected.train.confidence}% confidence</span></div><div className="route"><div className="route-stop"><span className="station-dot filled" /><span>{selected.train.current_station}</span></div><div className="route-line"><span style={{ width: `${selected.train.progress * 100}%` }} /></div><div className="route-stop next"><span className="station-dot" /><span>{selected.train.next_station}</span></div></div><div className="big-eta"><span>NEXT STATION ETA</span><strong>{formatEta(selected.eta)}</strong><small>{selected.eta_minutes} minutes from now</small></div><div className="conditions"><div><CloudRain size={18} /><span>Weather<strong>{selected.train.weather}</strong></span></div><div><Gauge size={18} /><span>Speed<strong>{selected.train.speed_kmph} km/h</strong></span></div><div><MapPin size={18} /><span>Distance<strong>{selected.train.distance_km} km</strong></span></div></div><div className="factors"><p className="eyebrow">WHY THIS ETA</p>{selected.factors.map((factor) => <p key={factor}>• {factor}</p>)}</div></> : <p className="empty">Select a service to inspect its forecast.</p>}</div>
      </section>
      <footer>RAIL/CAST · Forecast engine v0.1 · Designed for control room operations</footer>
    </main>
  );
}
