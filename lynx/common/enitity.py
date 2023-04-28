from __future__ import annotations
from dataclasses import dataclass

from lynx.common.serializable import Serializable


# right now it just represents common root for both `Object` and `Action`
class Entity(Serializable):
    @dataclass
    class _Exported(Serializable):
        type: str = ""
        attributes: str = ""

    def get_type(self) -> str:
        return type(self).__name__

    def get_attributes(self) -> str:
        return super().serialize()

    def serialize(self) -> str:
        return self._Exported(self.get_type(), self.get_attributes()).serialize()

    @classmethod
    def deserialize(cls, json_string: str) -> Entity:
        # we import every `Entity` type, so we can create instance of any of them when needed
        # TODO: simplify following imports
        from lynx.common.actions.move import Move
        from lynx.common.object import Object
        from lynx.common.actions.chop import Chop
        from lynx.common.actions.createObject import CreateObject
        from lynx.common.actions.removeObject import RemoveObject


        exported_entity = cls._Exported.deserialize(json_string)
        entity_type = locals()[exported_entity.type]
        entity = entity_type()
        entity.populate(exported_entity.attributes)
        return entity
