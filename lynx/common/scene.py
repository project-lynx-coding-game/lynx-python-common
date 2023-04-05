from typing import Dict, NoReturn, Optional

from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector


@dataclass
class Scene(Serializable):
    entities: List[Entity] = field(default_factory=list)
    _object_position_map: Dict[Vector, Object] = field(default_factory=dict)
    _object_id_map: Dict[int, Object] = field(default_factory=dict)

    def post_populate(self) -> NoReturn:
        for entity in self.entities:
            if type(entity) is Object:
                self._object_position_map[entity.position] = entity
                self._object_id_map[entity.id] = entity

    def add_entity(self, entity: Entity) -> NoReturn:
        self.entities.append(entity)
        if type(entity) is Object:
            self._object_position_map[entity.position] = entity
            self._object_id_map[entity.id] = entity

    def get_object_by_id(self, id: int) -> Optional[Object]:
        return self._object_id_map.get(id)

    def get_object_by_position(self, position: Vector) -> Optional[Object]:
        return self._object_map.get(position)

    def move_object(self, object: Object, vector: Vector) -> NoReturn:
        self._object_position_map[object.position] = None
        object.position = object.position + vector
        self._object_position_map[object.position] = object
