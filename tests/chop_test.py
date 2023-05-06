import random
from typing import NoReturn

from lynx.common.actions.action import Action
from lynx.common.actions.chop import Chop
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


class TestChopSerialization:
    expected_serialization_chop = '{"type": "Chop", "attributes": {"object_id": 1, "direction": {"x": 1, "y": 0}}}'

    def test_success_serialization(self) -> NoReturn:
        serialized_chop = Chop(object_id=1, direction=Vector(1, 0)).serialize()

        assert self.expected_serialization_chop == serialized_chop


class TestChopApply:
    def test_success_apply(self):
        random.seed(1222)
        expected_scene = Scene()
        expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        expected_dummy_chop = Chop(direction=Vector(0, 1), object_id=1)
        expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="Log", position=Vector(5, 6),
                                        pickable=True,  pushable=True, walkable=False)
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_chop)
        expected_scene.add_entity(expected_dummy_object2)

        random.seed(1222)
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_tree = Object(id=2, name="Tree", position=Vector(5, 6))
        dummy_chop = Chop(direction=Vector(0, 1), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_tree)
        scene.add_entity(dummy_chop)

        if dummy_chop.satisfies_requirements(scene):
            dummy_chop.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene


class TestChopRequirements:

    def test_success_requirements(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_tree = Object(id=2, name="Tree", position=Vector(5, 6))
        dummy_chop = Chop(direction=Vector(0, 1), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_tree)
        assert dummy_chop.satisfies_requirements(scene) is True

    def test_fail_requirements(self):
        scene = Scene()
        dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
        dummy_tree = Object(id=2, name="Tree", position=Vector(5, 6))
        dummy_chop = Chop(direction=Vector(1, 0), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_tree)
        assert dummy_chop.satisfies_requirements(scene) is not True
