from lynx.common.point import Point
from lynx.common.serializable import Properties
from lynx.common.objects.object import Object


class InteractiveObject(Object):
    """
    Abstract represents object that can interact with each other
    """
    base: str
    properties: Properties
    can_pick_up: bool

    def __init__(self, position: Point, scene: 'Scene') -> None:
        super().__init__(position, scene)
