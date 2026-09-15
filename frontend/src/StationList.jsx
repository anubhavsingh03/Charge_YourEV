function SourceBadge({ source }) {
  const isPartner = source !== 'ChargeList Directory';
  return (
    <span className={`source-badge ${isPartner ? 'partner' : 'directory'}`}>
      {source}
    </span>
  );
}

function StationList({ stations, onStart, activeSession }) {
  if (stations.length === 0) {
    return <div className="empty">No stations match this search.</div>;
  }

  return (
    <div className="listing">
      {stations.map((s) => {
        const isCharging = activeSession && activeSession.station_id === s.id && activeSession.status === 'charging';
        return (
          <div className="row" key={s.id}>
            <div className="row-main">
              <p className="row-title">{s.name}</p>
              <p className="row-meta">{s.city}{s.address ? ` · ${s.address}` : ''}</p>
              <div className="badges">
                {s.connectors.map((c) => <span className="badge" key={c}>{c}</span>)}
              </div>
              <SourceBadge source={s.source} />
            </div>
            <div className="row-side">
              {s.price != null && <p className="price">₹{s.price}/kWh</p>}
              {s.supports_session ? (
                <button
                  className={isCharging ? 'start-btn charging' : 'start-btn'}
                  disabled={isCharging}
                  onClick={() => onStart(s)}
                >
                  {isCharging ? 'Charging…' : 'Start charging'}
                </button>
              ) : (
                <a className="contact-btn" href={`tel:${s.phone}`}>Call {s.phone}</a>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default StationList;
