from typing import List

from lynx.common.object import Object
from lynx.common.square import Square
from lynx.common.vector import Vector
from lynx.common.enums import Direction
from lynx.common.scene import Scene

class CommonRequirements:

    @staticmethod
    def is_walkable(scene: 'Scene', position: Vector) -> bool:
        square_at_destination: Square = scene.get_square(position)
        return square_at_destination.walkable()

    @staticmethod
    def is_on_square(scene: 'Scene', position: Vector, name: str) -> bool:
        objects_on_square = scene.get_objects_by_position(position)
        return name in [object.name for object in objects_on_square]

    @staticmethod
    def is_any_on_square(scene: 'Scene', position: Vector, wanted_names: List[str]) -> bool:
        objects_on_square = scene.get_objects_by_position(position)
        objects_on_square_names = [object.name for object in objects_on_square]
        return any(name in objects_on_square_names for name in wanted_names)

    @staticmethod
    def is_in_range(scene: 'Scene', object_id: int, position: Vector, max_distance: int) -> bool:
        object: Object = scene.get_object_by_id(object_id)

        if object is None:
            return False

        distance = object.position.dist_to(position)
        return distance <= max_distance

    # object can be stacked on a given position if an object with the same name is already there
    @staticmethod
    def can_be_stacked(scene: 'Scene', position: Vector, object_name: str) -> bool:
        objects_on_square = scene.get_objects_by_position(position)

        for object in objects_on_square:
            if object.name == object_name:
                return True

        return False

    # TODO: Move, Push, Chop etc. should take argument of Direction type, not Vector type
    # this means that serialization and deserialization have to be adapted to Enum
    # when this is done, there is no need for this requirement
    @staticmethod
    def is_proper_direction(vector: Vector) -> bool:
        direction_vectors = [Direction.NORTH.value, Direction.SOUTH.value, Direction.EAST.value, Direction.WEST.value]
        return vector in direction_vectors

    @staticmethod
    def has_given_tags(scene: 'Scene', object_id: int, given_tags: List[str]) -> bool:
        object: Object = scene.get_object_by_id(object_id)

        if all(element in object.tags for element in given_tags):
            return True

        return False

    @staticmethod
    def any_object_on_square_has_all_given_tags(scene: Scene, position: Vector, given_tags: List[str]) -> bool:
        objects: List[Object] = scene.get_objects_by_position(position)
        for object in objects:
            if all(tag in object.tags for tag in given_tags):
                return True
        return False

    def has_something_in_inventory(scene: 'Scene', object_id: int) -> bool:
        object: Object = scene.get_object_by_id(object_id)
        return bool(object.inventory)
