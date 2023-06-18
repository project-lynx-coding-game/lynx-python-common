from dataclasses import dataclass, field
from typing import Dict

from lynx.common.actions.destroy_actions.destroy_around import Destroy_around


@dataclass
class Mine(Destroy_around):
    _object_to_drop_after_destroyment: Dict[str, str] = field(default_factory=lambda: {"Rock": "Stone"})
