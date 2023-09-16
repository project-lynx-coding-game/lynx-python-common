from typing import Dict, NoReturn, Optional

from lynx.common.square import Square
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector
from lynx.common.actions.create_object import CreateObject
from lynx.common.player import Player
import random


@dataclass
class Scene(Serializable):
    players: List[Player] = field(default_factory=list)
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

    def generate_id(self) -> int:
        MAX_ID = 1000000
        ids = list(self._object_id_map.keys())
        candidate_id = random.randint(0, MAX_ID)
        while candidate_id in ids:
            candidate_id = random.randint(0, MAX_ID)
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

    def add_to_pending_actions(self, action: str) -> NoReturn:
        self.pending_actions.append(action)

    def is_player_new(self, player_id: str) -> bool:
        players_id = [player.player_id for player in self.players]
        return player_id not in players_id

    def add_player(self, player: str) -> None:
        self.players.append(Player(player_id=player, player_resources={"Wood": 0, "Stone": 0}, drop_area=None))

    def is_world_created(self) -> bool:
        return bool(self.entities)

    def get_tile_positions(self) -> List[Vector]:
        tile_positions = []
        for position in self._square_position_map.keys():
            if self._square_position_map[position].tile():
                tile_positions.append(position)
        return tile_positions

    def generate_drop_area(self, player: str) -> None:
        tile_positions = self.get_tile_positions()
        position = random.choice(tile_positions)
        drop_area = Object(name="DropArea", id=self.generate_id(), position=position, owner=player)
        create_drop_area = CreateObject(drop_area.serialize())
        self.add_to_pending_actions(create_drop_area.serialize())
        player_object = self.get_player(player)
        player_object.drop_area = position

    def get_player(self, player_id: str) -> Optional[Player]:
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None

    def get_drop_area_of_a_player(self, player_id: str) -> Optional[Vector]:
        for player in self.players:
            if player.player_id == player_id:
                return player.drop_area
        return None

    def update_resources_of_player(self, player_id: str, inventory: Dict):
        player = self.get_player(player_id)
        for object_name, count in inventory.items():
            player.player_resources[object_name] += count
