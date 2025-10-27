from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from ..models import MachineState

@runtime_checkable
class Storage(Protocol):
    async def load(self) -> MachineState: ...
    async def save(self, state: MachineState) -> None: ...

class StorageBase(ABC):
    @abstractmethod
    async def load(self) -> MachineState: ...
    @abstractmethod
    async def save(self, state: MachineState) -> None: ...
