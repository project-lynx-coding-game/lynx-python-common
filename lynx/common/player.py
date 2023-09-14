from typing import Dict, NoReturn, Optional

from lynx.common.square import Square
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector
from lynx.common.serializable import Serializable

@dataclass
class Player(Serializable):
    player_id: str = field(default_factory=str)
    player_resources: Dict[str, int] = field(default_factory=dict)
    drop_area: Vector = field(default_factory=Vector)

