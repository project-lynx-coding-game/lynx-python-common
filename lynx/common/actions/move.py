from typing import NoReturn
from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements as Req
from lynx.common.object import Object
from lynx.common.vector import Vector
from lynx.common.enums import Direction


@dataclass
class Move(Action):
    """
    Simple action for changing position of `Object`. It does not log anything
    in case the movement was not possible (destination is not a tile etc).
    """
    object_id: int = -1
    direction: Vector = Direction.NORTH.value

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        destination_position = scene.get_object_by_id(self.object_id).position + self.direction
        return Req.is_tile(scene, destination_position) and Req.is_proper_direction(self.direction)

    def apply(self, scene: 'Scene') -> NoReturn:
        object: Object = scene.get_object_by_id(self.object_id)
        scene.move_object(object, self.direction)
