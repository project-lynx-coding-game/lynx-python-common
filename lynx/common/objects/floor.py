from lynx.common.vector import Vector
from lynx.common.objects.object import Object
from lynx.common.serializable import Properties


class Floor(Object):
    """
    Simple walkable `Object`.
    """
    base: str
    properties: Properties
    scene: 'Scene'
    walkable: bool

    def __init__(self, scene: 'Scene', position: Vector = Vector(0, 0)) -> None:
        super().__init__(position, scene)
        self.walkable = True
