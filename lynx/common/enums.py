from enum import Enum
from lynx.common.point import Point


class Direction(Enum):
    """
    Enumeration representing global directions
    """

    NORTH = Point(0, 1)
    EAST = Point(1, 0)
    SOUTH = Point(0, -1)
    WEST = Point(-1, 0)

    def __str__(self) -> str:
        if self == Direction.NORTH:
            return "NORTH"
        elif self == Direction.EAST:
            return "EAST"
        elif self == Direction.SOUTH:
            return "SOUTH"
        elif self == Direction.WEST:
            return "WEST"
