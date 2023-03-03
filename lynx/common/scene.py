from dataclasses import dataclass
from typing import List, Dict, NoReturn

from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector
from lynx.common.enitity import Entity


@dataclass
class Scene(Serializable):
    entities: List[Entity] = field(default_factory=list)
    _objects_map: Dict[Vector, Object] = field(default_factory=dict)

    def post_populate(self) -> NoReturn:
        for entity in self.entities:
            if type(entity) is Object:
                self._objects_map[entity.position] = entity

    def add_entity(self, entity: Entity) -> NoReturn:
        self.entities.append(entity)
        if type(entity) is Object:
            self._objects_map[entity.position] = entity
