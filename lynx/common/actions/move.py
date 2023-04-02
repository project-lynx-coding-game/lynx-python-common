from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.object import Object
from lynx.common.vector import Vector


@dataclass
class Move(Action):
    """
    Simple action for changing position of `Object`. It does not log anything
    in case the movement was not possible(destination is not walkable etc).
    """
    object_id: int = -1
    movement: Vector = Vector(0, 0)

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return CommonRequirements.is_walkable(scene, self.object_id, self.movement)

    def apply(self, scene: 'Scene') -> None:
        object: Object = scene.get_object_by_id(self.object_id)
        scene.move_object(object, self.movement)
