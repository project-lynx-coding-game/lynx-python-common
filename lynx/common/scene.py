
from dataclasses import dataclass
from typing import List
from lynx.common.objects.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector


@dataclass
class Scene(Serializable):
    objects: List[Object] = field(default_factory=list) 
    objects_map: dict[Vector, Object] = field(default_factory=dict) 

    # We are using separate class for serialization
    @dataclass
    class _ExportedScene(Serializable):
        types: List[str] = field(default_factory=list) 
        objects: List[str] = field(default_factory=list) 

    def serialize(self) -> str:
        types: List[str] = []
        objects: List[str] = []
        for object in self.objects:
            types.append(type(object).name)
            objects.append(object.serialize())

        exported = self._ExportedScene(types, objects)
        return exported.serialize()

    def populate(self, json_string) -> None:
        exported = self._ExportedScene.deserialize(json_string)
        
        for type, object_json in zip(exported.types, exported.objects):
            object_type = globals()[type]
            instance = object_type.deserialize(object_json)
            self.add_object(instance)

    def add_object(self, object: Object):
        self.objects.append(object)
        self.objects_map[object.position] = object

        