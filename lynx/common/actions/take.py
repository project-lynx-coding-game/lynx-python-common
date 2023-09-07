from dataclasses import dataclass, field
from typing import Dict

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.actions.create_object import CreateObject
from lynx.common.actions.remove_object import RemoveObject
from lynx.common.object import Object
from lynx.common.vector import Vector


@dataclass
class Take(Action):
    """
    Simple action for picking up objects, which can be picked up (pickable tag).
    After picking up, our inventory is updated for the amount of objects, which we picked. 
    """
    object_id: int = -1
    position: Vector = Vector(0, 1)


    def apply(self, scene: 'Scene') -> None:
        agent: Object = scene.get_object_by_id(self.object_id)
        objects_on_square = scene.get_objects_by_position(self.position)
        objects_to_pick = list(filter(lambda obj: obj.has_tags(["pickable"]), objects_on_square))
        for object_to_pick in objects_to_pick:
            remove_action = RemoveObject(object_to_pick.id)
            agent.add_to_inventory(object_to_pick.name)
            scene.add_to_pending_actions(remove_action.serialize())

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return CommonRequirements.is_in_range(scene, self.object_id, self.position, 1) \
               and CommonRequirements.any_object_on_square_has_all_given_tags(scene, self.position, ["pickable"])
