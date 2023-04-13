from typing import Dict, NoReturn, Optional

from lynx.common.square import Square
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector


@dataclass
class Scene(Serializable):
    entities: List[Entity] = field(default_factory=list)
    _square_position_map: Dict[Vector, Square] = field(default_factory=dict)
    _object_id_map: Dict[int, Object] = field(default_factory=dict)

    def _get_square(self, position: Vector) -> Square:
        # This method guarantees that the square is correct
        if square := self._square_position_map.get(position):
            return square

        new_square = Square()
        self._square_position_map[position] = new_square
        return new_square

    def _add_to_maps(self, entity: Entity) -> NoReturn:
        if type(entity) is Object:
            self._get_square(entity.position).append(entity)
            self._object_id_map[entity.id] = entity

    def post_populate(self) -> NoReturn:
        for entity in self.entities:
            self._add_to_maps(entity)

    def add_entity(self, entity: Entity) -> NoReturn:
        self.entities.append(entity)
        self._add_to_maps(entity)

    def get_object_by_id(self, id: int) -> Optional[Object]:
        return self._object_id_map.get(id)

    def get_objects_by_position(self, position: Vector) -> Optional[List[Object]]:
        return self._get_square(position).objects

    def move_object(self, object: Object, vector: Vector) -> NoReturn:
        self._get_square(object.position).remove(object)
        object.position = object.position + vector
        self._get_square(object.position).append(object)
