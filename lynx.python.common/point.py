import math


class Point:
    """
    Class representing 2D point
    """
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    # xxxXXXxxx WAAAAAAAAAARRRRRNINGGGGGGGG xxxXXXxxx
    # Position is passed to properties as string,
    # so frontends MUST parse the string on their own.
    # It's not another JSON dictionary for reasons.
    # That is - C# casting magic :)
    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    # For debugging purposes
    def __repr__(self):
        return str(self)

    def __add__(self, other):
        # Point type should be immutable
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def dist_to(self, point) -> float:
        # Euclidean distance from `self` to `point`
        dist: float = math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)
        return dist
