import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List

from database import Base, engine, SessionLocal
import models
import schemas
import normalizer
import adapters

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChargeList API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store — fine for a demo; would be a DB table in production
_sessions = {}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"status": "ok", "message": "ChargeList API is running"}


# ------------------------------------------------------------------
# Directory: agencies self-register (unchanged from before)
# ------------------------------------------------------------------
@app.post("/stations", response_model=schemas.StationOut)
def create_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    db_station = models.Station(
        name=station.name,
        city=station.city,
        address=station.address,
        connectors=",".join(station.connectors),
        price=station.price,
        phone=station.phone,
        email=station.email,
        latitude=station.latitude,
        longitude=station.longitude,
    )
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return _directory_to_out(db_station)


@app.get("/stations", response_model=List[schemas.StationOut])
def list_stations(city: Optional[str] = None, connector: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Unified station list: self-registered directory listings (source =
    'ChargeList Directory') PLUS every simulated partner network,
    normalized into the same shape.
    """
    query = db.query(models.Station)
    if city:
        query = query.filter(models.Station.city.ilike(f"%{city}%"))
    if connector:
        query = query.filter(models.Station.connectors.ilike(f"%{connector}%"))
    directory_stations = [_directory_to_out(s) for s in query.all()]

    partner_stations = normalizer.get_all_partner_stations()
    if city:
        partner_stations = [s for s in partner_stations if city.lower() in s.city.lower()]
    if connector:
        partner_stations = [s for s in partner_stations if connector in s.connectors]

    return directory_stations + partner_stations


def _directory_to_out(db_station: models.Station) -> schemas.StationOut:
    return schemas.StationOut(
        id=f"directory_{db_station.id}",
        name=db_station.name,
        city=db_station.city,
        address=db_station.address,
        connectors=db_station.connectors.split(",") if db_station.connectors else [],
        price=db_station.price,
        phone=db_station.phone,
        email=db_station.email,
        latitude=db_station.latitude,
        longitude=db_station.longitude,
        source="ChargeList Directory",
        supports_session=False,
    )


# ------------------------------------------------------------------
# Sessions: start/stop a charge through the unified layer — this is
# the part that only works for partner-network stations, since
# directory listings have no real hardware behind them.
# ------------------------------------------------------------------
@app.post("/sessions/start", response_model=schemas.SessionOut)
def start_session(req: schemas.SessionStartRequest):
    route = normalizer.route_for_station_id(req.station_id)
    if not route:
        raise HTTPException(
            status_code=400,
            detail="This station doesn't support remote session control (directory-only listing).",
        )
    start_fn, _ = route
    external_id = req.station_id.split("_", 1)[1]
    result = start_fn(external_id)

    session_id = str(uuid.uuid4())[:8]
    agency_name = next(
        (s.source for s in normalizer.get_all_partner_stations() if s.id == req.station_id),
        "Unknown",
    )
    _sessions[session_id] = {
        "session_id": session_id,
        "station_id": req.station_id,
        "agency": agency_name,
        "status": "charging",
        "started_at": adapters.now_iso(),
        "stopped_at": None,
    }
    return _sessions[session_id]


@app.post("/sessions/{session_id}/stop", response_model=schemas.SessionOut)
def stop_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    route = normalizer.route_for_station_id(session["station_id"])
    if route:
        _, stop_fn = route
        stop_fn(session_id)
    session["status"] = "completed"
    session["stopped_at"] = adapters.now_iso()
    return session


@app.get("/sessions/{session_id}", response_model=schemas.SessionOut)
def get_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
