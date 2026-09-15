import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

function MapView({ stations, onStart, activeSession }) {
  const withCoords = stations.filter((s) => s.latitude && s.longitude);
  const center = withCoords.length
    ? [withCoords[0].latitude, withCoords[0].longitude]
    : [18.5204, 73.8567];

  return (
    <div className="map-wrap">
      <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {withCoords.map((s) => {
          const isCharging = activeSession && activeSession.station_id === s.id && activeSession.status === 'charging';
          return (
            <Marker key={s.id} position={[s.latitude, s.longitude]}>
              <Popup>
                <strong>{s.name}</strong><br />
                {s.address}<br />
                {s.connectors.join(', ')}<br />
                {s.price != null ? `₹${s.price}/kWh` : ''}<br />
                <em>{s.source}</em><br />
                {s.supports_session ? (
                  <button disabled={isCharging} onClick={() => onStart(s)}>
                    {isCharging ? 'Charging…' : 'Start charging'}
                  </button>
                ) : (
                  <a href={`tel:${s.phone}`}>Call {s.phone}</a>
                )}
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
      {withCoords.length === 0 && (
        <p className="empty">No stations with location data match this search.</p>
      )}
    </div>
  );
}

export default MapView;
