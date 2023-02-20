from dataclasses import dataclass
import math
from lynx.common.serializable import Serializable


@dataclass(frozen=True)
class Vector(Serializable):
    """
    Class representing 2D point
    """
    x: int = 0
    y: int = 0

    # For debugging purposes
    def __repr__(self):
        return str(self)

    def __add__(self, other):
        # Point type should be immutable
        return Vector(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def dist_to(self, point) -> float:
        # Euclidean distance from `self` to `point`
        dist: float = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return dist
