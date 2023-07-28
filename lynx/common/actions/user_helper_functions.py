from dataclasses import dataclass
from typing import List


from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.object import Object


def objects_around(object_id: int, scene: 'Scene', distance: int) -> List[int]:
    selected_objects: List[int] = []
    agent_position: Vector = scene.get_object_by_id(object_id).position
    for obj in scene.entities:
        if obj.position.dist_to(agent_position) < distance:
            selected_objects.append(obj.id)
    return selected_objects


def get_position(scene: 'Scene',object_id: int) -> Vector:
    return scene.get_object_by_id(object_id).position


def get_type(scene: 'Scene',object_id: int) -> str:
    return scene.get_object_by_id(object_id).name


def distance_to(agent_id: int, scene: 'Scene', object_id: int) -> int:
    return scene.get_object_by_id(agent_id).position.dist_to(scene.get_object_by_id(object_id).position)


def fillter_list(scene: 'Scene', object_ids: List[int], object_type: str) -> List[int]:
    filltered_objects: List[int] = []
    for object_id in object_ids:
        if scene.get_object_by_id(object_id).name == object_type:
            filltered_objects.append(object_id)
    return filltered_objects