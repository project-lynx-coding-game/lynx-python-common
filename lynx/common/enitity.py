from __future__ import annotations
from dataclasses import dataclass, field

from lynx.common.serializable import Serializable


# right now it just represents common root for both `Object` and `Action`
class Entity(Serializable):
    @dataclass
    class _Exported(Serializable):
        type: str = ""
        attributes: dict = field(default_factory=dict)

    def get_type(self) -> str:
        return type(self).__name__

    def serialize(self) -> str:
        return self._Exported(self.get_type(), self.__dict__).serialize()

    @classmethod
    def deserialize(cls, json_string: str) -> Entity:
        # we import every `Entity` type, so we can create instance of any of them when needed
        # TODO: simplify following imports
        from lynx.common.actions.move import Move
        from lynx.common.object import Object
        from lynx.common.actions.chop import Chop
        from lynx.common.actions.mine import Mine
        from lynx.common.actions.push import Push
        from lynx.common.actions.message_log import MessageLog
        from lynx.common.actions.error_log import ErrorLog
        from lynx.common.actions.create_object import CreateObject
        from lynx.common.actions.remove_object import RemoveObject
        from lynx.common.actions.print import Print
        from lynx.common.actions.take import Take
        from lynx.common.actions.drop import Drop
        from lynx.common.actions.update_resources import UpdateResources
        from lynx.common.player import Player
        from lynx.common.agent import Agent

        exported_entity = cls._Exported.deserialize(json_string)
        entity_type = locals()[exported_entity.type]
        entity = entity_type()
        entity.populate(exported_entity.attributes)
        return entity
