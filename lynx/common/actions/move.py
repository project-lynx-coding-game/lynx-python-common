from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.object import Object
from lynx.common.vector import Vector
from lynx.common.enums import Direction


@dataclass
class Move(Action):
    """
    Simple action for changing position of `Object`. It does not log anything
    in case the movement was not possible(destination is not walkable etc).
    """
    object_id: int = -1
    direction: Vector = Direction.NORTH.value

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        destination_position = scene.get_object_by_id(self.object_id).position + self.direction
        return CommonRequirements.is_walkable(scene, destination_position)

    def apply(self, scene: 'Scene') -> None:
        object: Object = scene.get_object_by_id(self.object_id)
        scene.move_object(object, self.direction)
