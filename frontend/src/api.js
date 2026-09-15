const API_BASE = 'http://127.0.0.1:8000';

export async function fetchStations(city, connector) {
  const params = new URLSearchParams();
  if (city) params.set('city', city);
  if (connector) params.set('connector', connector);
  const res = await fetch(`${API_BASE}/stations?${params.toString()}`);
  return res.json();
}

export async function registerStation(payload) {
  const res = await fetch(`${API_BASE}/stations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Registration failed');
  return res.json();
}

export async function startSession(stationId) {
  const res = await fetch(`${API_BASE}/sessions/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ station_id: stationId }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Could not start session');
  }
  return res.json();
}

export async function stopSession(sessionId) {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/stop`, { method: 'POST' });
  if (!res.ok) throw new Error('Could not stop session');
  return res.json();
}

export { API_BASE };
