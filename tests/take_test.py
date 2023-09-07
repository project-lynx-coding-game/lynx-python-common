import random
from typing import NoReturn

from lynx.common.actions.action import Action
from lynx.common.actions.take import Take
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector
from lynx.common.enitity import Entity


class TestTakeSerialization:
    expected_serialization_take = '{"type": "Take", "attributes": {"object_id": 1, "position": {"x": 1, "y": 0}}}'

    def test_success_serialization(self) -> NoReturn:
        serialized_take = Take(object_id=1, position=Vector(1, 0)).serialize()
        assert self.expected_serialization_take == serialized_take

    def test_success_deserialization(self):
        expected_take = Take(object_id=1, position=Vector(1, 0))
        deserialized_take = Entity.deserialize(self.expected_serialization_take)
        assert expected_take == deserialized_take


class TestTakeApply:
    def test_apply_positive(self):
        expected_scene = Scene()
        expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        expected_dummy_take = Take(position=Vector(5, 6), object_id=1)
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_take)

        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_tree = Object(id=2, name="Wood", position=Vector(5, 6), tags=["pickable"])
        dummy_take = Take(position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_tree)
        scene.add_entity(dummy_take)

        dummy_take.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert expected_dummy_object == dummy_object
        assert scene.get_objects_by_position(Vector(5, 6)) == []

    def test_take_only_wood_from_square_with_multiple_objects_positive(self):
        expected_scene = Scene()
        expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_expected_tree = Object(id=3, name="Tree", position=Vector(5, 6))
        expected_dummy_take = Take(position=Vector(5, 6), object_id=1)
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_take)
        expected_scene.add_entity(dummy_expected_tree)

        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_wood = Object(id=2, name="Wood", position=Vector(5, 6), tags=["pickable"])
        dummy_tree = Object(id=3, name="Tree", position=Vector(5, 6))
        dummy_take = Take(position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_wood)
        scene.add_entity(dummy_take)
        scene.add_entity(dummy_tree)

        dummy_take.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene


class TestTakeRequirements:
    def test_all_requirements_satisifed_positive(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_wood = Object(id=2, name="Wood", position=Vector(5, 6), tags=["pickable"])
        dummy_tree = Object(id=3, name="Tree", position=Vector(5, 6))
        dummy_take = Take(position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_wood)
        scene.add_entity(dummy_tree)

        assert dummy_take.satisfies_requirements(scene)

    def test_take_single_wood_from_square_positive(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_wood = Object(id=2, name="Wood", position=Vector(5, 6), tags=["pickable"])
        dummy_tree = Object(id=3, name="Tree", position=Vector(5, 6))
        dummy_take = Take(position=Vector(5, 7), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_wood)
        scene.add_entity(dummy_tree)

        assert not dummy_take.satisfies_requirements(scene)

    def test_requirements_no_pickable_fail(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_tree = Object(id=3, name="Tree", position=Vector(5, 6))
        dummy_take = Take(position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_tree)

        assert not dummy_take.satisfies_requirements(scene)