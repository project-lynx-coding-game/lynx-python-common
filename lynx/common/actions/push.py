from typing import List, NoReturn
from dataclasses import dataclass, field

from lynx.common.vector import Vector
from lynx.common.actions.action import Action
from lynx.common.actions.move import Move
from lynx.common.actions.common_requirements import CommonRequirements as Req
from lynx.common.enums import Direction


@dataclass
class Push(Action):
    """
    Simple action used to push a pushable `Object` in given direction.
    """
    object_id: int = -1
    direction: Vector = Direction.NORTH.value
    pushed_object_ids: List[int] = field(default_factory=list)  # needed for deserialization to know what objects are being pushed

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        pushed_position = scene.get_object_by_id(self.object_id).position + self.direction  # position of pushed object
        destination_position = pushed_position + self.direction  # position to which the object is being pushed
        objects_on_square = scene.get_objects_by_position(pushed_position)

        for pushable_object in list(filter(lambda x: 'pushable' in x.tags, objects_on_square)):
            if Req.is_tile(scene, destination_position) or Req.can_be_stacked(scene, destination_position, pushable_object.name):
                self.pushed_object_ids.append(pushable_object.id)

        return Req.is_in_range(scene, self.object_id, pushed_position, 1) and Req.is_proper_direction(self.direction) and self.pushed_object_ids

    def apply(self, scene: 'Scene') -> NoReturn:
        pushed_position = scene.get_object_by_id(self.object_id).position + self.direction  # position of pushed object
        objects_on_square = scene.get_objects_by_position(pushed_position)

        for pushable_object in list(filter(lambda x: x.id in self.pushed_object_ids, objects_on_square)):
            Move(pushable_object.id, self.direction).apply(scene)
