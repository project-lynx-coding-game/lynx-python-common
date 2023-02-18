from lynx.common.enums import Direction
from lynx.common.vector import Vector
from lynx.common.actions.action import Action
from lynx.common.serializable import Properties
from lynx.common.objects.object import Object


class Move(Action):
    """
    Simple action for changing position of `Agent`. It does not log anything
    in case the movement was not possible(destination is not walkable etc).
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
        new_position: Vector = self.object.properties.position + self.properties.direction.value

        if not self.object.scene.move_object(self.object, new_position):
            return

        # Logging happens before collision detection
        # because it may result in loading next scene,
        # so we must ensure proper order of logs.
        self.log()

        self.object.scene.check_collisions(self.object)
