# ChargeList — Setup

## Backend
```
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic
uvicorn main:app --reload
```
Runs on http://127.0.0.1:8000 — API docs at /docs

## Frontend (new terminal)
```
cd frontend
npm install
npm run dev
```
Runs on http://localhost:5173

Both must run at the same time.

## What's here
- `backend/adapters.py` — three SIMULATED partner charging networks, each
  returning data in a deliberately different format (mirrors the real
  problem: every CPO formats data differently).
- `backend/normalizer.py` — converts all of them into one consistent shape.
  This is the core aggregation logic.
- `backend/main.py` — merges self-registered directory listings with all
  partner networks, plus /sessions/start and /sessions/{id}/stop.
- Frontend shows list + map views, search/filter, and a "Start charging"
  button on partner stations (directory listings show a Call button instead).

## Note
The three partner networks are simulated. Real integration requires API
partnership agreements with actual CPOs — the architecture here is what
you'd plug those into.
