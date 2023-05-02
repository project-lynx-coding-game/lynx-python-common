from typing import List
from dataclasses import dataclass, field

from lynx.common.object import Object
from lynx.common.vector import Vector
from lynx.common.actions.action import Action
from lynx.common.actions.move import Move
from lynx.common.actions.common_requirements import CommonRequirements


@dataclass
class Push(Action):
    """
    Simple action used to push a pushable `Object` in given direction.
    """
    object_id: int = -1
    # TODO: change to Direction type
    direction: Vector = Vector(1, 0)
    # needed for deserialization to know what objects are being pushed
    pushed_object_ids: List[int] = field(default_factory=list)

    def apply(self, scene: 'Scene') -> None:
        target_position = scene.get_object_by_id(self.object_id).position + self.direction
        objects_on_square = scene.get_objects_by_position(target_position)
        for pushable_object in filter(lambda x: x.pushable, objects_on_square):
            Move(object_id=pushable_object.id, movement=self.direction).apply(scene)
            self.pushed_object_ids.append(pushable_object.id)

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        target_position = scene.get_object_by_id(self.object_id).position + self.direction
        return CommonRequirements.is_in_range(scene, self.object_id, target_position, 1) and CommonRequirements.is_pushable(scene, target_position)
