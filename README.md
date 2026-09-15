# ChargeYourEV

Solving the "one app per charging network" problem for EV owners in India.

EV drivers in India currently have to download a separate app for nearly every charging network they use — Tata Power, Statiq, ChargeZone, and dozens of regional operators each run their own siloed app and payment system. ChargeYourEV aggregates them into a single interface: search for a station, compare pricing and connector types across networks, and start a charging session without switching apps.

## How it works

- **Unified station directory** — independent charging agencies can self-register their stations (name, location, connectors, pricing, contact).
- **Partner network aggregation** — a normalization layer ingests data from multiple charging networks, each with a different raw API format, and merges them into one consistent interface. (Currently simulated with three mock partner APIs to demonstrate the integration architecture — real deployment would connect this layer to live CPO partnership APIs.)
- **Unified session control** — for partner-connected networks, users can start and stop a charging session directly through the app instead of switching to the operator's own app.
- **Map and list search** — filter by city and connector type (CCS2, Type 2, CHAdeMO, GB/T, Bharat AC001), view results as a list or on an interactive map.

## Tech stack

**Backend:** FastAPI, SQLAlchemy, SQLite, Pydantic
**Frontend:** React (Vite), react-leaflet, OpenStreetMap

## Architecture

The normalization layer is the core piece: it is built so that swapping a simulated adapter for a real CPO's API is a contained change — the rest of the app (frontend, session logic, search) does not need to know or care where the data came from.

## Running locally

See SETUP.md.

## Status

Working proof of concept. Real deployment would require formal API and data-sharing partnerships with charging network operators — the current partner networks are simulated to demonstrate the aggregation architecture end-to-end.
