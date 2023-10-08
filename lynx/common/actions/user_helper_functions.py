import random
from typing import List

from lynx.common.actions.common_requirements import CommonRequirements as Req
from lynx.common.vector import Vector


def get_objects_around(object_id: int, scene: 'Scene', distance: int) -> List[int]:
    """Gets the ids of the objects around the object.

    Args:
        object_id: The id of the object.
        scene: The scene.
        distance: The distance from the object.

    Returns:
        The ids of the objects around the object.

    """
    selected_objects_ids: List[int] = []
    agent_position: Vector = scene.get_object_by_id(object_id).position
    for obj in scene.entities:
        if obj.position.manhattan_distance(agent_position) <= distance:
            selected_objects_ids.append(obj.id)
    selected_objects_ids.remove(object_id)
    return selected_objects_ids


def get_position(scene: 'Scene', object_id: int) -> Vector:
    """Returns the position of the object.

    Args:
        scene: The scene.
        object_id: The id of the object.

    Returns:
        The position of the object.

    """
    return scene.get_object_by_id(object_id).position


def get_number_of_items_in_inventory(scene: 'Scene', object_id: int) -> int:
    """Returns number of objects in inventory

    Args:
        scene: The scene.
        object_id: The id of the object.

    Returns:
        The number of objects in inventory

    """
    return sum(scene.get_object_by_id(object_id).inventory.values())


def can_i_stand(scene: 'Scene', position: Vector) -> bool:
    """Returns True if the position is a tile.

    Args:
        scene: The scene.
        position: The position.

    Returns:
        True if the position is a tile.

    """
    return Req.is_tile(scene, position)


def get_type(scene: 'Scene', object_id: int) -> str:
    """Returns the type of the object.

    Args:
        scene: The scene.
        object_id: The id of the object.

    Returns:
        The type of the object.

    """
    return scene.get_object_by_id(object_id).name


def calculate_distance_to(scene: 'Scene', object_id: int, agent_id: int) -> int:
    """Returns the Manhattan distance between two objects.

    Args:
        scene: The scene.
        object_id: The id of the first object.
        agent_id: The id of the second object.

    Returns:
        The Manhattan distance between two objects.
    """
    return scene.get_object_by_id(agent_id).position.manhattan_distance(scene.get_object_by_id(object_id).position)


def filter_objects(scene: 'Scene', object_ids: List[int], object_type: str) -> List[int]:
    """Returns a list of object ids of the given type.

    Args:
        scene: The scene.
        object_ids: The list of object ids to filter.
        object_type: The type of the objects to filter.

    Returns:
        The list of object ids of the given type.

    """
    filtered_objects_ids: List[int] = list(
        filter(lambda object_id: scene.get_object_by_id(object_id).name == object_type, object_ids)
    )
    return filtered_objects_ids


def random_direction(scene: 'Scene', object_id: int) -> Vector:
    """Returns a random direction from the list of available directions.

    Args:
        scene: The scene.
        object_id: The id of the object.

    Returns:
        A random direction from the list of available directions.
    """
    positions: List[Vector] = [Vector(0, 1), Vector(1, 0), Vector(-1, 0), Vector(0, -1)]
    object_position: Vector = scene.get_object_by_id(object_id).position
    available_positions = list(
        filter(lambda position: Req.is_tile(scene, object_position + position), positions)
    )
    return random.choice(available_positions)
