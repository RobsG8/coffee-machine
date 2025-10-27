# ☕ Coffee Machine — FastAPI + Vue 3

## Project Overview
A **FastAPI backend** with a **Vue 3 frontend**, simulating a simple coffee machine.

### Features
- Recipes: **Espresso**, **Double Espresso**, **Americano**, **Ristretto**
- Human-readable errors for **empty**, **insufficient**, **overflow**, or **unknown drink**
- **Pluggable persistence** via `STORAGE_BACKEND` → `memory` | `json` | `sqlite`
- UI displays live status messages & errors from the API
- Supports **state persistence**, **overflow checks**, and **status endpoints**
- Includes **unit tests** and **Postman collections** for validation

---

## Assumptions
- Default capacities: **Water 2000 ml**, **Coffee 500 g** (modifiable through state)
- `fill` endpoints **add** to current values, not set them absolutely
- The **Ristretto** recipe is implemented and available via the API/UI

---

## Run with Docker
```bash
# In project root directory

# Choose persistence backend (memory | json | sqlite)
# Example for PowerShell:
$Env:STORAGE_BACKEND = "sqlite"

docker compose up --build
```

**Endpoints:**
- Backend → [http://localhost:8000/docs](http://localhost:8000/docs)
- Frontend → [http://localhost:5173](http://localhost:5173)

---

## Local Development

### Backend
```bash
cd backend
python -m venv .venv && .\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm i
npm run dev
```

---

## Tests
```bash
docker compose run --rm backend pytest -q
# Expected output: 5 passed
```

---

## Postman Collection
Import the following from `/postman/`:

| File |
|------|
| `CoffeeMachine.postman_collection.json` |

**Required collection variable:**
```
baseUrl = http://localhost:8000
```

**Other variables:**
```
waterAmount = 1000
coffeeAmount = 100
brewType = espresso
brewList = espresso,double_espresso,americano,ristretto
```

---

## Switching Storage Backend
```bash
# PowerShell example
$Env:STORAGE_BACKEND = "json"     # or memory | sqlite
docker compose up --build
```

**Persistence details:**
- JSON → `/data/state.json` (via Docker volume)
- SQLite → `/data/state.db`

---

## Troubleshooting (Windows)
- Use **Docker Desktop** with WSL2 backend.
- If Docker CLI says “can’t connect”:
  ```bash
  wsl --status
  # Then start Docker Desktop
  docker context use desktop-linux
  ```
- If frontend buttons don’t respond:
  - Check for free ports **5173** (frontend) and **8000** (backend).

---

## Quick Summary
| Component | Tech Stack | Purpose |
|------------|-------------|----------|
| Backend | FastAPI | Brewing logic, persistence, validation |
| Frontend | Vue 3 + Vite | Interactive UI |
| Storage | Memory / JSON / SQLite | Pluggable data persistence |
| Testing | Pytest + Postman | Functional and integration testing |
