from typing import Union


from lynx.python.common.actions.action import Action
from lynx.python.common.serializable import Properties
from lynx.python.common.objects.npc import NPC


class Destroy(Action):
    """
    Simple action for dying.
    """
    base: str
    properties: Properties
    object: Union['Agent', NPC]

    def __init__(self, object: Union['Agent', NPC]) -> None:
        super().__init__()
        self.properties.object_id = object.properties.id
        self.object = object

    def execute(self) -> None:
        self.object.scene.remove_object_from_occupied_fields(self.object)
        self.object.scene.remove_object_from_id_map(self.object)
        self.log()
