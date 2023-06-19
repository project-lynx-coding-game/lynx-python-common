from dataclasses import dataclass, field
from typing import Dict

from lynx.common.actions.destroy_actions.destroy_around import DestroyAround


@dataclass
class Mine(DestroyAround):
    _object_to_drop_after_destruction: Dict[str, str] = field(default_factory=lambda: {"Rock": "Stone"})
