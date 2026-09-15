import { useState, useEffect, useCallback } from 'react';
import MapView from './MapView';
import StationList from './StationList';
import RegisterForm from './RegisterForm';
import SessionBar from './SessionBar';
import { fetchStations, startSession, stopSession } from './api';
import './App.css';

function App() {
  const [tab, setTab] = useState('browse');
  const [view, setView] = useState('list'); // list | map
  const [stations, setStations] = useState([]);
  const [cityQuery, setCityQuery] = useState('');
  const [connectorQuery, setConnectorQuery] = useState('');
  const [activeSession, setActiveSession] = useState(null);
  const [error, setError] = useState('');

  const loadStations = useCallback(async () => {
    const data = await fetchStations(cityQuery, connectorQuery);
    setStations(data);
  }, [cityQuery, connectorQuery]);

  useEffect(() => {
    loadStations();
  }, [loadStations]);

  const handleStart = async (station) => {
    setError('');
    try {
      const session = await startSession(station.id);
      setActiveSession({ ...session, stationName: station.name });
    } catch (e) {
      setError(e.message);
    }
  };

  const handleStop = async () => {
    if (!activeSession) return;
    const updated = await stopSession(activeSession.session_id);
    setActiveSession({ ...activeSession, ...updated });
    setTimeout(() => setActiveSession(null), 2500);
  };

  return (
    <div className="app">
      <div className="topbar">
        <div className="brand">Charge<span>List</span></div>
        <div className="tabs">
          <button className={tab === 'browse' ? 'active' : ''} onClick={() => setTab('browse')}>
            Find charging
          </button>
          <button className={tab === 'register' ? 'active' : ''} onClick={() => setTab('register')}>
            List your station
          </button>
        </div>
      </div>

      {activeSession && <SessionBar session={activeSession} onStop={handleStop} />}

      {tab === 'browse' && (
        <section className="browse">
          <div className="browse-head">
            <h1>Charging stations, one app.</h1>
            <p>Directory listings plus live-connected partner networks — search, compare, and start a session without switching apps.</p>
          </div>

          <div className="filters">
            <input
              type="text"
              placeholder="Search by city…"
              value={cityQuery}
              onChange={(e) => setCityQuery(e.target.value)}
            />
            <select value={connectorQuery} onChange={(e) => setConnectorQuery(e.target.value)}>
              <option value="">Any connector</option>
              <option value="CCS2">CCS2</option>
              <option value="Type 2">Type 2</option>
              <option value="CHAdeMO">CHAdeMO</option>
              <option value="GB/T">GB/T</option>
              <option value="Bharat AC001">Bharat AC001</option>
            </select>
            <div className="view-toggle">
              <button className={view === 'list' ? 'active' : ''} onClick={() => setView('list')}>List</button>
              <button className={view === 'map' ? 'active' : ''} onClick={() => setView('map')}>Map</button>
            </div>
          </div>

          {error && <p className="error-banner">{error}</p>}

          {view === 'list'
            ? <StationList stations={stations} onStart={handleStart} activeSession={activeSession} />
            : <MapView stations={stations} onStart={handleStart} activeSession={activeSession} />}
        </section>
      )}

      {tab === 'register' && (
        <RegisterForm onSuccess={loadStations} />
      )}
    </div>
  );
}

export default App;
