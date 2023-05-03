from typing import List
from dataclasses import dataclass, field

from lynx.common.vector import Vector
from lynx.common.actions.action import Action
from lynx.common.actions.move import Move
from lynx.common.actions.common_requirements import CommonRequirements as Req


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
        pushed_position = scene.get_object_by_id(self.object_id).position + self.direction
        objects_on_square = scene.get_objects_by_position(pushed_position)

        for pushable_object in filter(lambda x: x.id in self.pushed_object_ids, objects_on_square):
            Move(object_id=pushable_object.id, movement=self.direction).apply(scene)

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        pushed_position = scene.get_object_by_id(self.object_id).position + self.direction
        destination_position = pushed_position + self.direction
        objects_on_square = scene.get_objects_by_position(pushed_position)

        for pushable_object in filter(lambda x: x.pushable, objects_on_square):
            if Req.is_walkable(scene, destination_position) or Req.is_stackable(scene, destination_position, pushable_object.name):
                self.pushed_object_ids.append(pushable_object.id)

        return Req.is_in_range(scene, self.object_id, pushed_position, 1) and self.pushed_object_ids
