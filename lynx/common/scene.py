
from dataclasses import dataclass
from typing import List
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector

@dataclass
class _ExportedEntity(Serializable):
    type: str = ""
    args: str = ""

# We are using separate class for serialization
@dataclass
class _ExportedScene(Serializable):
    entities: List[_ExportedEntity] = field(default_factory=list) 

@dataclass
class Scene(Serializable):
    _entities: List[Entity] = field(default_factory=list) 
    objects_map: dict[Vector, Object] = field(default_factory=dict) 


    def serialize(self) -> str:
        exported_entities: List[_ExportedEntity] = []
        for entity in self._entities:
            exported_entity = _ExportedEntity(type=type(entity).name, args=entity.serialize())
            exported_entities.append(exported_entity)

        exported = _ExportedScene(exported_entities)
        return exported.serialize()

    def populate(self, json_string) -> None:
        exported = _ExportedScene.deserialize(json_string)
        
        for exported_entity in exported.entities:
            object_type = globals()[exported_entity.type]
            instance = object_type.deserialize(exported_entity.args)
            if type(instance) is Object:
                self.add_object(instance)

    def add_entity(self, entity: Entity):
        self._entities.append(entity)

    def add_object(self, object: Object):
        self.add_entity(object)
        self.objects_map[object.position] = object

        