from dataclasses import dataclass, field
from typing import Dict

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.actions.create_object import CreateObject
from lynx.common.actions.remove_object import RemoveObject
from lynx.common.enums import Direction
from lynx.common.object import Object
from lynx.common.vector import Vector


@dataclass
class DestroyAround(Action):
    """
    Simple action used to hit/destroy object, which stands on the given destination.
    """
    object_id: int = -1
    # target_position: Vector = Vector(1, 0) # Currently we want to chop the tree in specific direction
    direction: Vector = Direction.NORTH.value
    # Dictionary, which has object name and what it will drop e.g. "
    _object_to_drop_after_destroyment: Dict[int, str] = field(default_factory=dict)


    def apply(self, scene: 'Scene') -> None:
        target_position = self._get_target_position(scene)
        objects_on_square = scene.get_objects_by_position(target_position)
        x = self._object_to_drop_after_destroyment.keys
        destroyed_object_iterator = iter(list(filter(lambda object_on_square: object_on_square.name in self._object_to_drop_after_destroyment.keys(), objects_on_square)))
        destroyed_object = next(destroyed_object_iterator, None)
        if destroyed_object:
            remove_action = RemoveObject(destroyed_object.id)
            log = Object(id=scene.generate_id(), name= self._object_to_drop_after_destroyment[destroyed_object.name], tags=['pushable', 'pickable'],
                         position=destroyed_object.position)
            create_action = CreateObject(log.serialize())
            scene.add_to_pending_actions(remove_action.serialize())
            scene.add_to_pending_actions(create_action.serialize())

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return CommonRequirements.is_in_range(scene, self.object_id, self._get_target_position(scene), 1) \
               and CommonRequirements.is_any_on_square(scene, self._get_target_position(scene), self._object_to_drop_after_destroyment.keys())

    def _get_target_position(self, scene: 'Scene') -> Vector:
        return scene.get_object_by_id(self.object_id).position + self.direction
