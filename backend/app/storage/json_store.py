import json, asyncio, os
from .base import StorageBase
from ..models import MachineState

class JsonStore(StorageBase):
    def __init__(self, path: str = "/data/state.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    async def load(self) -> MachineState:
        if not os.path.exists(self.path):
            return MachineState()
        # use thread to avoid blocking
        content = await asyncio.to_thread(lambda: open(self.path, "r", encoding="utf-8").read())
        data = json.loads(content)
        return MachineState(**data)

    async def save(self, state: MachineState) -> None:
        payload = state.model_dump()
        await asyncio.to_thread(lambda: open(self.path, "w", encoding="utf-8").write(json.dumps(payload, indent=2)))
