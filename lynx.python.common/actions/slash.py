from lynx.python.common.enums import Direction
from lynx.python.common.point import Point
from lynx.python.common.actions.action import Action
from lynx.python.common.actions.deal_dmg import DealDmg
from lynx.python.common.serializable import Properties
from lynx.python.common.objects.object import Object
from lynx.python.common.objects.npcs.enemy import Enemy

SLASH_DMG = 100


class Slash(Action):
    """
    Simple action for attacking.
    """
    base: str
    properties: Properties
    object: Object

    def __init__(self, object: Object, direction: Direction) -> None:
        super().__init__()
        self.properties.object_id = object.properties.id
        self.object = object
        self.properties.direction = direction

    def execute(self) -> None:
        self.log()
        target_position: Point = self.object.properties.position + self.properties.direction.value
        for target in self.object.scene.get_objects_by_position(target_position):
            if isinstance(target, Enemy):
                DealDmg(target, 100).execute()
