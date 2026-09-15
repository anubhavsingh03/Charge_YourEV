"""
Simulated third-party charging network APIs.

In a real deployment, each of these functions would instead make an HTTP
request to that agency's actual API. Every agency deliberately returns data
in a different shape here — this mirrors the real-world problem: every CPO
in India formats its data differently, which is exactly why a unifying
layer (see normalizer.py) is the hard part of building an aggregator.
"""
import random
import string
import datetime

# ---------------------------------------------------------------------
# Agency A — "VoltGrid" style: flat fields, comma-separated connectors
# ---------------------------------------------------------------------
_AGENCY_A_STATIONS = [
    {
        "id": 101,
        "station_name": "VoltGrid Koregaon Park",
        "town": "Pune",
        "addr": "Lane 5, Koregaon Park",
        "plug_types": "CCS2,Type 2",
        "unit_price": 19.5,
        "contact_no": "9900011122",
        "lat": 18.5362,
        "lng": 73.8938,
    },
    {
        "id": 102,
        "station_name": "VoltGrid Hinjewadi Phase 1",
        "town": "Pune",
        "addr": "IT Park Road, Hinjewadi",
        "plug_types": "CCS2",
        "unit_price": 21.0,
        "contact_no": "9900011133",
        "lat": 18.5912,
        "lng": 73.7389,
    },
]

def fetch_agency_a():
    return _AGENCY_A_STATIONS


def start_session_agency_a(external_id: str):
    return {"ok": True, "reference": f"A-{external_id}-{_rand_suffix()}"}


def stop_session_agency_a(reference: str):
    return {"ok": True}


# ---------------------------------------------------------------------
# Agency B — "Statiq-like" style: nested objects, list of connector dicts
# ---------------------------------------------------------------------
_AGENCY_B_STATIONS = [
    {
        "stationId": "STQ-4471",
        "title": "Statiq Viman Nagar Mall",
        "location": {
            "city": "Pune",
            "address": "Viman Nagar Road",
            "coordinates": {"latitude": 18.5679, "longitude": 73.9143},
        },
        "connectors": [{"type": "CCS2"}, {"type": "CHAdeMO"}],
        "tariff": 18.0,
        "ownerPhone": "9911122233",
    },
    {
        "stationId": "STQ-4488",
        "title": "Statiq Magarpatta City",
        "location": {
            "city": "Pune",
            "address": "Magarpatta Cybercity",
            "coordinates": {"latitude": 18.5158, "longitude": 73.9280},
        },
        "connectors": [{"type": "Type 2"}],
        "tariff": 17.5,
        "ownerPhone": "9911122244",
    },
]

def fetch_agency_b():
    return _AGENCY_B_STATIONS


def start_session_agency_b(external_id: str):
    return {"success": True, "sessionRef": f"B-{external_id}-{_rand_suffix()}"}


def stop_session_agency_b(reference: str):
    return {"success": True}


# ---------------------------------------------------------------------
# Agency C — "BharatCharge" style: geo as [lat, lng] array, different keys
# ---------------------------------------------------------------------
_AGENCY_C_STATIONS = [
    {
        "charger_id": "BC-77",
        "name": "BharatCharge Kothrud Depot",
        "geo": [18.5074, 73.8077],
        "city_name": "Pune",
        "full_address": "Paud Road, Kothrud",
        "connector_list": ["GB/T", "Bharat AC001"],
        "rate_per_unit": 16.0,
        "helpline": "9922233344",
    },
]

def fetch_agency_c():
    return _AGENCY_C_STATIONS


def start_session_agency_c(external_id: str):
    return {"status": "OK", "session": f"C-{external_id}-{_rand_suffix()}"}


def stop_session_agency_c(reference: str):
    return {"status": "OK"}


def _rand_suffix():
    return "".join(random.choices(string.digits, k=4))


def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"
