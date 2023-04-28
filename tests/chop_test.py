import unittest
from typing import NoReturn

from lynx.common.actions.chop import Chop
from lynx.common.actions.action import Action
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector
import random

class TestChopSerialization:
	expected_serialization_chop = '{"type": "Chop", "attributes": "{\\"position\\": {\\"x\\": 2, \\"y\\": 2}, \\"object_id\\": 1}"}'

	def test_success_serialization(self) -> NoReturn:
		serialized_chop = Chop(object_id=1, position=Vector(2, 2)).serialize()

		assert self.expected_serialization_chop == serialized_chop


class TestChopApply:
	def test_success_apply(self):
		random.seed(1222)
		expected_scene = Scene()
		expected_dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
		expected_dummy_chop = Chop(position=Vector(5, 6), object_id=1)
		expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="log", position=Vector(5, 6), pickable = True)
		expected_scene.add_entity(expected_dummy_object)
		expected_scene.add_entity(expected_dummy_chop)
		expected_scene.add_entity(expected_dummy_object2)

		random.seed(1222)
		scene = Scene()
		dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
		dummy_tree = Object(id=2, name="tree", position=Vector(5, 6))
		dummy_chop = Chop(position=Vector(5, 6), object_id=1)
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_tree)
		scene.add_entity(dummy_chop)
		dummy_chop.apply(scene)
		for action in scene.pending_actions:
			Action.deserialize(action).apply(scene)
		scene.pending_actions.clear()

		assert scene == expected_scene

class TestChopRequirements:
	def test_success_requirements(self):
		scene = Scene()
		dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
		dummy_tree = Object(id=2, name="tree", position=Vector(5, 6))
		dummy_chop = Chop(position=Vector(5, 6), object_id=1)
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_tree)
		assert dummy_chop.satisfies_requirements(scene) is True

	def test_fail_requirements(self):
		scene = Scene()
		dummy_object = Object(id=1, name="dummy", position=Vector(5, 5))
		dummy_tree = Object(id=2, name="tree", position=Vector(5, 6))
		dummy_chop = Chop(position=Vector(5, 3), object_id=1)
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_tree)
		assert dummy_chop.satisfies_requirements(scene) is not True
