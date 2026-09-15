from pydantic import BaseModel
from typing import Optional, List

class StationCreate(BaseModel):
    name: str
    city: str
    address: Optional[str] = None
    connectors: List[str]
    price: Optional[float] = None
    phone: str
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StationOut(BaseModel):
    id: str
    name: str
    city: str
    address: Optional[str] = None
    connectors: List[str]
    price: Optional[float] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    source: str
    supports_session: bool = False

class SessionStartRequest(BaseModel):
    station_id: str

class SessionOut(BaseModel):
    session_id: str
    station_id: str
    agency: str
    status: str
    started_at: str
    stopped_at: Optional[str] = None
