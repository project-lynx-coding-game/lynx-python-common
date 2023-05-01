import unittest
from typing import NoReturn

from lynx.common.actions.take import Take
from lynx.common.actions.action import Action
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector
import random

class TestTakeSerialization:
	expected_serialization_take = ('{"type": "Take", "attributes": "{\\"object_id\\": 1, \\"object_to_pick\\": \\"Log\\"}"}')

	def test_success_serialization(self) -> NoReturn:
		serialized_take = Take(object_id=1, object_to_pick= 'Log').serialize()

		assert self.expected_serialization_take == serialized_take


class TestChopApply:
	def test_success_apply(self):
		expected_scene = Scene()
		expected_dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5), inventory= [2])
		expected_dummy_take = Take(object_id= 1, object_to_pick='Log')
		expected_dummy_log = Object(id=2, name="Log", position=Vector(5, 5), pickable = True, hidden= True)

		expected_scene.add_entity(expected_dummy_object)
		expected_scene.add_entity(expected_dummy_log)
		expected_scene.add_entity(expected_dummy_take)
		expected_scene.remove_from_map(expected_dummy_log)

		scene = Scene()
		dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5))
		dummy_log = Object(id=2, name="Log", position=Vector(5, 5), pickable = True)
		dummy_take = Take(object_id=1, object_to_pick='Log')
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_log)
		scene.add_entity(dummy_take)
		dummy_take.apply(scene)
		for action in scene.pending_actions:
			Action.deserialize(action).apply(scene)
		scene.pending_actions.clear()

		assert scene == expected_scene

	def test_success_multiple_objects_apply(self):
		expected_scene = Scene()
		expected_dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5), inventory=[2])
		expected_dummy_take = Take(object_id=1, object_to_pick='Log')
		expected_dummy_log = Object(id=2, name="Log", position=Vector(5, 5), pickable=True, hidden=True)
		expected_dummy_log2 = Object(id=3, name="Log", position=Vector(5, 5), pickable=True)

		expected_scene.add_entity(expected_dummy_object)
		expected_scene.add_entity(expected_dummy_log)
		expected_scene.add_entity(expected_dummy_log2)
		expected_scene.add_entity(expected_dummy_take)
		expected_scene.remove_from_map(expected_dummy_log)

		scene = Scene()
		dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5))
		dummy_log = Object(id=2, name="Log", position=Vector(5, 5), pickable=True)
		dummy_log2 = Object(id=3, name="Log", position=Vector(5, 5), pickable=True)
		dummy_take = Take(object_id=1, object_to_pick='Log')
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_log)
		scene.add_entity(dummy_log2)
		scene.add_entity(dummy_take)
		dummy_take.apply(scene)
		for action in scene.pending_actions:
			Action.deserialize(action).apply(scene)
		scene.pending_actions.clear()

		assert scene == expected_scene


class TestChopRequirements:
	def test_success_requirements(self):
		scene = Scene()
		dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5))
		dummy_log = Object(id=2, name="Log", position=Vector(5, 5), pickable = True)
		dummy_take = Take(object_id=1, object_to_pick='Log')
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_log)
		assert dummy_take.satisfies_requirements(scene) is True

	def test_fail_requirements(self):
		scene = Scene()
		dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5))
		dummy_log = Object(id=2, name="Diff_object", position=Vector(5, 5), pickable=True)
		dummy_take = Take(object_id=1, object_to_pick='Log')
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_log)
		assert dummy_take.satisfies_requirements(scene) is not True

	def test_fail_is_not_pickable(self):
		scene = Scene()
		dummy_object = Object(id=1, name="Dummy", position=Vector(5, 5))
		dummy_log = Object(id=2, name="Log", position=Vector(5, 5))
		dummy_take = Take(object_id=1, object_to_pick='Log')
		scene.add_entity(dummy_object)
		scene.add_entity(dummy_log)
		assert dummy_take.satisfies_requirements(scene) is not True

