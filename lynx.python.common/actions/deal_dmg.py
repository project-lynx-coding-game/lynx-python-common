from typing import Union

from lynx.python.common.actions.action import Action
from lynx.python.common.actions.destroy import Destroy
from lynx.python.common.serializable import Properties
from lynx.python.common.objects.npc import NPC


class DealDmg(Action):
    """
    Simple action for dealing damage.
    """
    base: str
    properties: Properties
    target: Union['Agent', NPC]

    def __init__(self, target: Union['Agent', NPC], dmg: int) -> None:
        super().__init__()
        self.properties.object_id = target.properties.id
        self.target = target
        self.properties.dmg = dmg

    def execute(self) -> None:
        self.target.hp -= self.properties.dmg
        self.log()
        if self.target.hp <= 0:
            Destroy(self.target).execute()
