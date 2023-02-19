from dataclasses import dataclass
from typing import List

from lynx.common.vector import Vector
from lynx.common.enums import Direction
from lynx.common.serializable import Serializable, Properties


@dataclass
class Object(Serializable):
    """
    Abstract object existing in a `scene`. Represents part of scene's state,
    in contrast to `Action` which represents only modifications of the state.
    """

    id: int = -1
    name: str = "Object"
    position: Vector = Vector(0, 0)
    walkable: bool = False
    tick: str = ""
    on_death: str = ""

    def occupied_fields(self, current_position: Vector = None) -> List[Vector]:
        if not current_position:
            current_position = self.properties.position
        return [current_position]
