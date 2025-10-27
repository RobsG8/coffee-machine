import os
from functools import lru_cache 
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import MachineState, BrewRequest, FillWaterRequest, FillCoffeeRequest, Message
from .errors import HumanReadableError
from .domain import brew, fill_water, fill_coffee, RECIPES
from .storage.base import Storage
from .storage.memory_store import MemoryStore
from .storage.json_store import JsonStore
from .storage.sqlite_store import SqliteStore

@lru_cache
def get_store() -> Storage:
    backend = os.getenv("STORAGE_BACKEND", "memory").lower()
    if backend == "json":
        return JsonStore(path=os.getenv("JSON_PATH", "/data/state.json"))
    if backend == "sqlite":
        return SqliteStore(path=os.getenv("SQLITE_PATH", "/data/state.db"))
    return MemoryStore()

app = FastAPI(title="Coffee Machine API", version="1.0.0")

# Frontend uses Vite dev server; allow local hosts
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

async def with_state(store: Storage = Depends(get_store)) -> tuple[Storage, MachineState]:
    state = await store.load()
    return store, state

@app.get("/api/status", response_model=MachineState)
async def status(dep=Depends(with_state)):
    _, state = dep
    return state

@app.post("/api/fill/water", response_model=Message)
async def fill_water_ep(req: FillWaterRequest, dep=Depends(with_state)):
    store, state = dep
    try:
        new_state = fill_water(state, req.amount_ml)
        await store.save(new_state)
        return Message(message=f"Filled {req.amount_ml} ml water.", state=new_state)
    except HumanReadableError as e:
        raise e
    except Exception as e:
        raise HumanReadableError(f"Unexpected error while filling water: {e}")

@app.post("/api/fill/coffee", response_model=Message)
async def fill_coffee_ep(req: FillCoffeeRequest, dep=Depends(with_state)):
    store, state = dep
    try:
        new_state = fill_coffee(state, req.amount_g)
        await store.save(new_state)
        return Message(message=f"Filled {req.amount_g} g coffee.", state=new_state)
    except HumanReadableError as e:
        raise e
    except Exception as e:
        raise HumanReadableError(f"Unexpected error while filling coffee: {e}")

@app.post("/api/brew", response_model=Message)
async def brew_ep(req: BrewRequest, dep=Depends(with_state)):
    store, state = dep
    try:
        new_state = brew(state, req.type)
        await store.save(new_state)
        return Message(message=f"Enjoy your {req.type.replace('_',' ')}!", state=new_state)
    except HumanReadableError as e:
        raise e
    except Exception as e:
        raise HumanReadableError(f"Unexpected error while brewing: {e}")

# Specific endpoints for convenience / explicitness
@app.post("/api/brew/espresso", response_model=Message)
async def brew_espresso(dep=Depends(with_state)):
    return await brew_ep(BrewRequest(type="espresso"), dep)

@app.post("/api/brew/double-espresso", response_model=Message)
async def brew_double(dep=Depends(with_state)):
    return await brew_ep(BrewRequest(type="double_espresso"), dep)

@app.post("/api/brew/americano", response_model=Message)
async def brew_americano(dep=Depends(with_state)):
    return await brew_ep(BrewRequest(type="americano"), dep)

@app.post("/api/brew/ristretto", response_model=Message)
async def brew_ristretto(dep=Depends(with_state)):
    return await brew_ep(BrewRequest(type="ristretto"), dep)

@app.get("/api/recipes")
async def recipes():
    return RECIPES
