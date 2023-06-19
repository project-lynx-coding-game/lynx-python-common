from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.object import Object


@dataclass
class RemoveObject(Action):
    """
    Remove objects from the game
    """
    # TODO: put all special values into an Enum
    object_id: int = -1

    def apply(self, scene: 'Scene') -> None:
        object: Object = scene.get_object_by_id(self.object_id)
        scene.remove_object(object)

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return scene.get_object_by_id(self.object_id) is not None
