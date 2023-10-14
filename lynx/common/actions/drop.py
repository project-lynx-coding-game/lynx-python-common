from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.actions.create_object import CreateObject
from lynx.common.actions.update_resources import UpdateResources
from lynx.common.object import Object
from lynx.common.vector import Vector


@dataclass
class Drop(Action):
    """
    Action used to empty inventory of Agent.
    If target_position is equal to drop_area_position, we should increase global points and resources.
    If target_position is different than drop_area_position then we should create each object from inventory on chosen
    square (target_position)
    """
    object_id: int = -1
    target_position: Vector = Vector(0, 1)

    def drop_in_drop_area(self, scene: 'Scene', player_name: str, inventory: dict):
        scene.update_resources_of_player(player_name, inventory)
        update_resources_action = UpdateResources(player_name, inventory)
        scene.add_to_pending_actions(update_resources_action.serialize())

    def drop_in_overworld(self, scene: 'Scene', inventory: dict):
        for objects_to_drop in inventory:
            for object_to_drop in range(inventory[objects_to_drop]):
                object_created = Object(id=scene.generate_id(),
                                        name=objects_to_drop,
                                        tags=['pushable', 'pickable'],
                                        position=self.target_position)
                create_action = CreateObject(object_created.serialize())
                scene.add_to_pending_actions(create_action.serialize())

    def apply(self, scene: 'Scene') -> None:
        agent: Object = scene.get_object_by_id(self.object_id)
        player_name = agent.owner
        player = scene.get_player(agent.owner)
        if self.target_position == scene.get_drop_area_of_a_player(player_name):
            self.drop_in_drop_area(scene, player_name, agent.inventory)
        else:
            self.drop_in_overworld(scene, agent.inventory)

        agent.inventory = {}
        player.get_agent_by_id(agent.id).drop_inventory()

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        agent: Object = scene.get_object_by_id(self.object_id)

        return CommonRequirements.is_in_range(scene, self.object_id, self.target_position, 1) \
            and (CommonRequirements.is_tile(scene, self.target_position)
                 or scene.get_drop_area_of_a_player(agent.owner) == self.target_position) \
            and CommonRequirements.has_something_in_inventory(scene, self.object_id)
