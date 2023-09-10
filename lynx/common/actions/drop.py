from dataclasses import dataclass
from collections import defaultdict

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.actions.create_object import CreateObject
from lynx.common.actions.update_points import UpdatePoints
from lynx.common.object import Object
from lynx.common.vector import Vector


@dataclass
class Drop(Action):
    """
    Action used to empty inventory of agent.
    If target_position is equal to drop_area_position, we should increase global points and resources.
    If target_position is different than drop_area_position then we should create each object from inventory on choosen
    square (target_position)
    """
    object_id: int = -1
    target_position: Vector = Vector(0, 1)

    def apply(self, scene: 'Scene') -> None:
        agent: Object = scene.get_object_by_id(self.object_id)
        player_name = agent.owner
        if self.target_position == scene.get_drop_area_of_a_player(player_name):
            scene.update_resources_of_player(player_name, agent.inventory)
            updated_points_action = UpdatePoints(player_name, agent.inventory)
            scene.add_to_pending_actions(updated_points_action.serialize())
        else:
            for objects_to_drop in agent.inventory:
                for object_to_drop in range(agent.inventory[objects_to_drop]):
                    object_created = Object(id=scene.generate_id(),
                                            name=objects_to_drop,
                                            tags=['pushable', 'pickable'],
                                            position=self.target_position)
                    create_action = CreateObject(object_created.serialize())
                    scene.add_to_pending_actions(create_action.serialize())

        agent.inventory = {}

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        agent: Object = scene.get_object_by_id(self.object_id)

        return CommonRequirements.is_in_range(scene, self.object_id, self.target_position, 1) \
                and (CommonRequirements.is_walkable(scene, self.target_position)
                     or scene.get_drop_area_of_a_player(agent.owner) == self.target_position) \
                and CommonRequirements.has_something_in_inventory(scene, self.object_id)