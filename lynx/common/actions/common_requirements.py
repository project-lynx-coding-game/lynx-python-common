from lynx.common.object import Object
from lynx.common.square import Square
from lynx.common.vector import Vector


class CommonRequirements:

    @staticmethod
    def is_walkable(scene: 'Scene', object_id: int, movement: Vector) -> bool:
        object: Object = scene.get_object_by_id(object_id)
        destination_position: Vector = object.position + movement
        square_at_destination: Square = scene.get_square(destination_position)
        return square_at_destination.walkable()
