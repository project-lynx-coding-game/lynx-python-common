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
    walkable: bool = False
    tick: str = ""
    on_death: str = ""
    owner: str = ""
    pickable: bool = False
    hidden: bool = False    #Idk if we need this, because maybe it will be enough just not to have this on square list
    inventory:  List[int] = field(default_factory=list)
