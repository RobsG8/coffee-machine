import aiosqlite, os
from .base import StorageBase
from ..models import MachineState

SCHEMA = """
CREATE TABLE IF NOT EXISTS machine_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    water_ml INTEGER NOT NULL,
    coffee_g INTEGER NOT NULL,
    water_capacity_ml INTEGER NOT NULL,
    coffee_capacity_g INTEGER NOT NULL
);
"""

class SqliteStore(StorageBase):
    def __init__(self, path: str = "/data/state.db"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    async def _ensure(self):
        async with aiosqlite.connect(self.path) as db:
            await db.execute(SCHEMA)
            await db.execute(
                "INSERT OR IGNORE INTO machine_state (id, water_ml, coffee_g, water_capacity_ml, coffee_capacity_g) "
                "VALUES (1, 0, 0, 2000, 500)"
            )
            await db.commit()

    async def load(self) -> MachineState:
        await self._ensure()
        async with aiosqlite.connect(self.path) as db:
            cur = await db.execute("SELECT water_ml, coffee_g, water_capacity_ml, coffee_capacity_g FROM machine_state WHERE id=1")
            row = await cur.fetchone()
            return MachineState(
                water_ml=row[0], coffee_g=row[1],
                water_capacity_ml=row[2], coffee_capacity_g=row[3]
            )

    async def save(self, state: MachineState) -> None:
        await self._ensure()
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "UPDATE machine_state SET water_ml=?, coffee_g=?, water_capacity_ml=?, coffee_capacity_g=? WHERE id=1",
                (state.water_ml, state.coffee_g, state.water_capacity_ml, state.coffee_capacity_g)
            )
            await db.commit()
