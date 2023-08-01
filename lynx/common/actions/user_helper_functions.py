import random
from typing import List


from lynx.common.vector import Vector
from lynx.common.actions.common_requirements import CommonRequirements as Req


def objects_around(object_id: int, scene: 'Scene', distance: int) -> List[int]:
    selected_objects: List[int] = []
    agent_position: Vector = scene.get_object_by_id(object_id).position
    for obj in scene.entities:
        if obj.position.manhattan_distance(agent_position) <= distance:
            selected_objects.append(obj.id)
    selected_objects.remove(object_id)
    return selected_objects


def get_position(scene: 'Scene', object_id: int) -> Vector:
    return scene.get_object_by_id(object_id).position


def can_i_stand(scene: 'Scene', positon: Vector) -> bool:
    return Req.is_walkable(scene, positon)


def get_type(scene: 'Scene', object_id: int) -> str:
    return scene.get_object_by_id(object_id).name


def distance_to(scene: 'Scene', object_id: int, agent_id: int) -> int:
    return scene.get_object_by_id(agent_id).position.manhattan_distance(scene.get_object_by_id(object_id).position)


def filter_objects(scene: 'Scene', object_ids: List[int], object_type: str) -> List[int]:
    filtered_objects: List[int] = []
    for object_id in object_ids:
        if scene.get_object_by_id(object_id).name == object_type:
            filtered_objects.append(object_id)
    return filtered_objects


def random_direction(scene: 'Scene', object_id: int) -> Vector:
    positions: List[Vector] = [Vector(0, 1), Vector(1, 0), Vector(-1, 0), Vector(0, -1)]
    available_positions: List[Vector] = []
    object_position: Vector = scene.get_object_by_id(object_id).position
    for position in positions:
        if Req.is_walkable(scene, object_position + position):
            available_positions.append(position)
    random_choice = random.choice(available_positions)
    return random_choice
