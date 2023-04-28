from typing import Dict, NoReturn, Optional

from lynx.common.square import Square
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector
import random


@dataclass
class Scene(Serializable):
    entities: List[Entity] = field(default_factory=list)
    pending_actions: List[str] = field(default_factory=list)  # Transformations which occur, during other transformations (e.g. chop -> Create logs)
    _square_position_map: Dict[Vector, Square] = field(default_factory=dict)
    _object_id_map: Dict[int, Object] = field(default_factory=dict)

    def get_square(self, position: Vector) -> Square:
        # This method guarantees that the square is correct
        if square := self._square_position_map.get(position):
            return square

        new_square = Square()
        self._square_position_map[position] = new_square
        return new_square

    def _add_to_maps(self, entity: Entity) -> NoReturn:
        if type(entity) is Object:
            self.get_square(entity.position).append(entity)
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
        return self.get_square(position).objects

    def generate_id(self):
        max_id_number = 1000000
        ids = list(self._object_id_map.keys())
        candidate_id = random.randint(0, max_id_number)
        while candidate_id in ids:
            candidate_id = random.randint(0, max_id_number)
        return candidate_id

    def move_object(self, object: Object, vector: Vector) -> NoReturn:
        self.get_square(object.position).remove(object)
        object.position = object.position + vector
        self.get_square(object.position).append(object)

    def remove_object(self, object: Object) -> NoReturn:
        self.get_square(object.position).remove(object)
        self.entities.remove(object)
        self._object_id_map.pop(object.id)
        del object

    def add_to_pending_actions(self, action: str):
        self.pending_actions.append(action)
