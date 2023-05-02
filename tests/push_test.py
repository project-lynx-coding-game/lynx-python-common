from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.push import Push
from lynx.common.enums import Direction
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.enitity import Entity
from lynx.common.vector import Vector
from lynx.common.actions.action import Action


class TestPushSerialization:
    expected_serialized_push = '{"type": "Push", "attributes": "{\\"object_id\\": 123, \\"direction\\": {\\"x\\": -1, \\"y\\": 0}}"}'

    def test_success(self) -> NoReturn:
        serialized_push = Push(object_id=123, direction=Direction.WEST.value).serialize()
        assert serialized_push == self.expected_serialized_push

    def test_failure(self) -> NoReturn:
        serialized_push = Push(object_id=123, direction=Direction.EAST.value).serialize()
        assert serialized_push != self.expected_serialized_push


class TestMoveDeserialization:
    expected_deserialized_push = Push(object_id=123, direction=Direction.WEST.value)

    def test_success(self) -> NoReturn:
        serialized_push = '{"type": "Push", "attributes": "{\\"object_id\\": 123, \\"direction\\": {\\"x\\": -1, \\"y\\": 0}}"}'
        deserialized_push = Push.deserialize(serialized_push)

        assert deserialized_push == self.expected_deserialized_push

    def test_failure(self) -> NoReturn:
        serialized_push = '{"type": "Push", "attributes": "{\\"object_id\\": 345, \\"direction\\": {\\"x\\": 1, \\"y\\": 0}}"}'
        deserialized_push = Push.deserialize(serialized_push)

        assert deserialized_push != self.expected_deserialized_push


class TestPushSatisfiesRequirements:
    def test_satisfies(self) -> NoReturn:
        scene = Scene()
        pushable_object = Object(id=123, name="dummy", position=Vector(1, 1), pushable=True)
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        scene.add_entity(pushable_object)
        scene.add_entity(pusher_object)
        scene.add_entity(dummy_action)

        assert dummy_action.satisfies_requirements(scene)


class TestPushApply:
    def test_apply(self) -> NoReturn:
        expected_scene = Scene()
        expected_pushable_object = Object(id=123, name="dummy", position=Vector(0, 1), pushable=True)
        expected_pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        expected_dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        expected_scene.add_entity(expected_pushable_object)
        expected_scene.add_entity(expected_pusher_object)
        expected_scene.add_entity(expected_dummy_action)

        scene = Scene()
        pushable_object = Object(id=123, name="dummy", position=Vector(1, 1), pushable=True)
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        scene.add_entity(pushable_object)
        scene.add_entity(pusher_object)
        scene.add_entity(dummy_action)
        dummy_action.apply(scene)

        assert len(scene.pending_actions) == 1
        
        Entity.deserialize(scene.pending_actions[0]).apply(scene)

        assert expected_pushable_object == pushable_object
        assert scene.get_objects_by_position(Vector(0, 1)) == [pushable_object]
        assert scene.get_objects_by_position(Vector(1, 1)) == []
