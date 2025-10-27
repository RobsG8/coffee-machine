from .base import StorageBase
from ..models import MachineState

class MemoryStore(StorageBase):
    def __init__(self, initial: MachineState | None = None):
        self._state = initial or MachineState()

    async def load(self) -> MachineState:
        return self._state

    async def save(self, state: MachineState) -> None:
        self._state = state
