"""
Converts each agency's raw, differently-shaped data into one consistent
StationOut shape the frontend can render identically, regardless of source.
This normalization step is the core value of an aggregator app.
"""
import adapters
from schemas import StationOut


def normalize_agency_a(raw: dict) -> StationOut:
    return StationOut(
        id=f"agencya_{raw['id']}",
        name=raw["station_name"],
        city=raw["town"],
        address=raw["addr"],
        connectors=raw["plug_types"].split(","),
        price=raw["unit_price"],
        phone=raw["contact_no"],
        latitude=raw["lat"],
        longitude=raw["lng"],
        source="VoltGrid (partner network)",
        supports_session=True,
    )


def normalize_agency_b(raw: dict) -> StationOut:
    loc = raw["location"]
    coords = loc["coordinates"]
    return StationOut(
        id=f"agencyb_{raw['stationId']}",
        name=raw["title"],
        city=loc["city"],
        address=loc["address"],
        connectors=[c["type"] for c in raw["connectors"]],
        price=raw["tariff"],
        phone=raw["ownerPhone"],
        latitude=coords["latitude"],
        longitude=coords["longitude"],
        source="Statiq (partner network)",
        supports_session=True,
    )


def normalize_agency_c(raw: dict) -> StationOut:
    lat, lng = raw["geo"]
    return StationOut(
        id=f"agencyc_{raw['charger_id']}",
        name=raw["name"],
        city=raw["city_name"],
        address=raw["full_address"],
        connectors=raw["connector_list"],
        price=raw["rate_per_unit"],
        phone=raw["helpline"],
        latitude=lat,
        longitude=lng,
        source="BharatCharge (partner network)",
        supports_session=True,
    )


def get_all_partner_stations():
    """Fetches from every simulated agency and normalizes into one list."""
    out = []
    for raw in adapters.fetch_agency_a():
        out.append(normalize_agency_a(raw))
    for raw in adapters.fetch_agency_b():
        out.append(normalize_agency_b(raw))
    for raw in adapters.fetch_agency_c():
        out.append(normalize_agency_c(raw))
    return out


# Maps a unified station id's prefix back to the right adapter's
# start/stop functions, so /sessions/start can route correctly.
_AGENCY_ROUTES = {
    "agencya": (adapters.start_session_agency_a, adapters.stop_session_agency_a),
    "agencyb": (adapters.start_session_agency_b, adapters.stop_session_agency_b),
    "agencyc": (adapters.start_session_agency_c, adapters.stop_session_agency_c),
}


def route_for_station_id(station_id: str):
    prefix = station_id.split("_", 1)[0]
    return _AGENCY_ROUTES.get(prefix)
