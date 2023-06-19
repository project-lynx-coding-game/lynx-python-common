from dataclasses import dataclass, field
from typing import List

from lynx.common.enitity import Entity
from lynx.common.vector import Vector


@dataclass
class Object(Entity):
    """
    `Object` existing in a `Scene`.
    Represents part of `Scene`'s state, in contrast to `Action` which represents only modifications of the state.
    Always set name to `Object` type in constructor.
    """

    id: int = -1
    name: str = "Object"
    position: Vector = Vector(0, 0)
    additional_positions: List[Vector] = field(default_factory=list) 
    state: str = ""
    tick: str = ""
    on_death: str = ""
    owner: str = ""
    tags: List[str] = field(default_factory=list)

    def has_tags(self, given_tags: List[str]):
        if all(element in self.tags for element in given_tags):
            return True

        return False
