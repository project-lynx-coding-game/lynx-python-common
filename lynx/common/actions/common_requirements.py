from lynx.common.object import Object
from lynx.common.vector import Vector


class CommonRequirements:

    @staticmethod
    def is_walkable(scene: 'Scene', object_id: int, movement: Vector) -> bool:
        object: Object = scene.get_object_by_id(object_id)
        destination_position: Vector = object.position + movement
        object_at_destination: Object = scene.get_object_by_position(destination_position)
        return object_at_destination is not None and object_at_destination.walkable
