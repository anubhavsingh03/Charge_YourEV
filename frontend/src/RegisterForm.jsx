import { useState } from 'react';
import { registerStation } from './api';

const CONNECTOR_OPTIONS = ['CCS2', 'Type 2', 'CHAdeMO', 'GB/T', 'Bharat AC001'];

function RegisterForm({ onSuccess }) {
  const [form, setForm] = useState({
    name: '', city: '', address: '', price: '', phone: '', email: '',
    latitude: null, longitude: null,
  });
  const [connectors, setConnectors] = useState([]);
  const [status, setStatus] = useState('');

  const toggleConnector = (c) => {
    setConnectors((prev) => (prev.includes(c) ? prev.filter((x) => x !== c) : [...prev, c]));
  };

  const useMyLocation = () => {
    if (!navigator.geolocation) {
      setStatus('Geolocation not supported by this browser.');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setForm((f) => ({ ...f, latitude: pos.coords.latitude, longitude: pos.coords.longitude }));
        setStatus('Location captured.');
      },
      () => setStatus('Could not get location — check browser permissions.')
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (connectors.length === 0) {
      setStatus('Select at least one connector type.');
      return;
    }
    try {
      await registerStation({
        name: form.name,
        city: form.city,
        address: form.address || null,
        connectors,
        price: form.price ? parseFloat(form.price) : null,
        phone: form.phone,
        email: form.email || null,
        latitude: form.latitude,
        longitude: form.longitude,
      });
      setStatus('Station listed successfully.');
      setForm({ name: '', city: '', address: '', price: '', phone: '', email: '', latitude: null, longitude: null });
      setConnectors([]);
      onSuccess();
    } catch {
      setStatus('Something went wrong — check the fields.');
    }
  };

  return (
    <section className="form-wrap">
      <h1>Register your station</h1>
      <p>Add your charging point so EV owners searching ChargeList can find and contact you directly.</p>

      <form onSubmit={handleSubmit} className="register-form">
        <label htmlFor="name">Agency / operator name</label>
        <input id="name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />

        <label htmlFor="city">City</label>
        <input id="city" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} required />

        <label htmlFor="address">Address</label>
        <input id="address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />

        <label>Connector types</label>
        <div className="chip-group">
          {CONNECTOR_OPTIONS.map((c) => (
            <div key={c} className={`chip ${connectors.includes(c) ? 'on' : ''}`} onClick={() => toggleConnector(c)}>
              {c}
            </div>
          ))}
        </div>

        <label htmlFor="price">Price per unit (₹/kWh)</label>
        <input id="price" type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} />

        <label htmlFor="phone">Phone</label>
        <input id="phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} required />

        <label htmlFor="email">Email</label>
        <input id="email" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />

        <button type="button" className="location-btn" onClick={useMyLocation}>
          📍 Use my current location {form.latitude ? '✓' : ''}
        </button>

        <button type="submit" className="submit-btn">List this station</button>

        {status && <p className="status">{status}</p>}
      </form>
    </section>
  );
}

export default RegisterForm;
