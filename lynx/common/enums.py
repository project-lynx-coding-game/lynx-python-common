from enum import Enum
from lynx.common.vector import Vector


class Direction(Enum):
    """
    Enumeration representing global directions
    """

    NORTH = Vector(0, 1)
    EAST = Vector(1, 0)
    SOUTH = Vector(0, -1)
    WEST = Vector(-1, 0)

    def __str__(self) -> str:
        if self == Direction.NORTH:
            return "NORTH"
        elif self == Direction.EAST:
            return "EAST"
        elif self == Direction.SOUTH:
            return "SOUTH"
        elif self == Direction.WEST:
            return "WEST"
