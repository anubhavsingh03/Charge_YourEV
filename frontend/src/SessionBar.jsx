function SessionBar({ session, onStop }) {
  const isDone = session.status === 'completed';
  return (
    <div className={`session-bar ${isDone ? 'done' : ''}`}>
      <div>
        <strong>{isDone ? 'Session complete' : 'Charging in progress'}</strong>
        <span> — {session.stationName || session.station_id} ({session.agency})</span>
      </div>
      {!isDone && <button onClick={onStop}>Stop charging</button>}
    </div>
  );
}

export default SessionBar;
