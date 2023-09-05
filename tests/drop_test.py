import random
from typing import NoReturn

from lynx.common.actions.action import Action
from lynx.common.actions.drop import Drop
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


class TestDropSerialization:
    expected_serialization_drop = '{"type": "Drop", "attributes": {"object_id": 1, "target_position": {"x": 1, "y": 0}, "drop_area_position": {"x": 1, "y": 0}}}'

    def test_success_serialization(self) -> NoReturn:
        serialized_drop = Drop(object_id=1, target_position=Vector(1, 0), drop_area_position=Vector(1, 0)).serialize()

        assert self.expected_serialization_drop == serialized_drop

    def test_success_deserialization(self):
        expected_drop = Drop(object_id=1, target_position=Vector(1, 0), drop_area_position=Vector(1, 0))
        dummy_drop = Drop.deserialize(self.expected_serialization_drop)

        assert dummy_drop == expected_drop

class TestDropApply:
    def test_success_apply(self):
        random.seed(1222)
        expected_scene = Scene()
        expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        expected_dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(0, 0))
        expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_drop)
        expected_scene.add_entity(expected_dummy_object2)

        random.seed(1222)
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(0, 0))
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_drop)

        dummy_drop.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene

    def test_success_multiple_objects_apply(self):
        random.seed(1222)
        expected_scene = Scene()
        expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        expected_dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(0, 0))
        expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_dummy_object3 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_dummy_object4 = Object(id=expected_scene.generate_id(), name="Stone", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_drop)
        expected_scene.add_entity(expected_dummy_object2)
        expected_scene.add_entity(expected_dummy_object3)
        expected_scene.add_entity(expected_dummy_object4)

        random.seed(1222)
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 2, "Stone": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(0, 0))
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_drop)

        dummy_drop.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene

class TestDropRequirements:

    def test_success_requirements(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(5, 6))
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is True

    def test_fail_requirements_distance(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(6, 6), object_id=1, drop_area_position=Vector(5, 8))
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True

    def test_fail_requirements_inventory(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(5, 8))
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True

    def test_fail_requirements_walkable(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1, drop_area_position=Vector(5, 8))
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6)))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True
