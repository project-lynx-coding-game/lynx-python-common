from dataclasses import dataclass, field
from datetime import datetime

from lynx.common.serializable import Serializable


@dataclass
class Agent(Serializable):
    id: int = -1
    type: str = ""
    time_creation: str | None = None
    time_death: str | None = None
    is_alive: bool = True
    tick: str = ""
    lifetime: float | None = None
    inventory: dict[str, int] = field(default_factory=dict)
    historical_inventory: dict[str, int] = field(default_factory=dict)

    def calculate_lifetime(self) -> float:
        time = datetime.now() if self.time_death is None else datetime.fromisoformat(self.time_death)
        return (time - datetime.fromisoformat(self.time_creation)).total_seconds()

    def drop_inventory(self):
        self.inventory = {}

    def add_to_inventory(self, object_name: str):
        self.update_inventory(object_name, self.inventory)
        self.update_inventory(object_name, self.historical_inventory)

    @staticmethod
    def update_inventory(object_name: str, inventory: dict[str, int]):
        if object_name in inventory:
            inventory[object_name] += 1
        else:
            inventory[object_name] = 1
