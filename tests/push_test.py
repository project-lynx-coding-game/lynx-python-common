from typing import NoReturn

from lynx.common.actions.push import Push
from lynx.common.enums import Direction
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


class TestPushSerialization:
    expected_serialized_push = '{"type": "Push", "attributes": {"object_id": 123, "direction": {"x": -1, "y": 0}, ' \
                               '"pushed_object_ids": [1, 2, 3]}}'

    def test_success(self) -> NoReturn:
        push = Push(object_id=123, direction=Direction.WEST.value)
        push.pushed_object_ids = [1, 2, 3]
        serialized_push = push.serialize()
        assert serialized_push == self.expected_serialized_push

    def test_failure(self) -> NoReturn:
        push = Push(object_id=456, direction=Direction.EAST.value)
        push.pushed_object_ids = [4, 5, 6]
        serialized_push = push.serialize()
        assert serialized_push != self.expected_serialized_push


class TestPushDeserialization:
    expected_deserialized_push = Push(object_id=123, direction=Direction.WEST.value)
    expected_deserialized_push.pushed_object_ids = [1, 2, 3]

    def test_success(self) -> NoReturn:
        serialized_push = '{"type": "Push", "attributes": {"object_id": 123, "direction": {"x": -1, "y": 0}, ' \
                          '"pushed_object_ids": [1, 2, 3]}}'
        deserialized_push = Push.deserialize(serialized_push)

        assert deserialized_push == self.expected_deserialized_push

    def test_failure(self) -> NoReturn:
        serialized_push = '{"type": "Push", "attributes": {"object_id": 456, "direction": {"x": 1, "y": 0}, ' \
                          '"pushed_object_ids": [4, 5, 6]}}'
        deserialized_push = Push.deserialize(serialized_push)

        assert deserialized_push != self.expected_deserialized_push


class TestPushSatisfiesRequirements:
    def test_square_tile_satisfies(self) -> NoReturn:
        scene = Scene()
        pushable_object = Object(id=123, name="dummy", position=Vector(1, 1), tags=['pushable'])
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        tile_object = Object(id=789, name="dummy123", position=Vector(0, 1), tags=['tile'])
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        scene.add_entity(pushable_object)
        scene.add_entity(pusher_object)
        scene.add_entity(tile_object)
        scene.add_entity(dummy_action)

        assert dummy_action.satisfies_requirements(scene)

    def test_square_not_tile_taken_by_same_object_satisfies(self) -> NoReturn:
        scene = Scene()
        pushable_object = Object(id=123, name="dummy", position=Vector(1, 1), tags=['pushable'])
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        blocking_object = Object(id=789, name="dummy", position=Vector(0, 1))
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        scene.add_entity(pushable_object)
        scene.add_entity(pusher_object)
        scene.add_entity(blocking_object)
        scene.add_entity(dummy_action)

        assert dummy_action.satisfies_requirements(scene)

    def test_square_not_tile_taken_by_different_object_does_not_satisfy(self) -> NoReturn:
        scene = Scene()
        pushable_object = Object(id=123, name="dummy", position=Vector(1, 1), tags=['pushable'])
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        blocking_object = Object(id=789, name="dummy123", position=Vector(0, 1))
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        scene.add_entity(pushable_object)
        scene.add_entity(pusher_object)
        scene.add_entity(blocking_object)
        scene.add_entity(dummy_action)

        assert not dummy_action.satisfies_requirements(scene)


class TestPushApply:
    def test_apply(self) -> NoReturn:
        expected_scene = Scene()
        expected_pushable_object1 = Object(id=123, name="dummy", position=Vector(0, 1), tags=['pushable'])
        expected_pushable_object2 = Object(id=12, name="dummy", position=Vector(0, 1), tags=['pushable'])
        expected_pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        expected_dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        expected_dummy_action.pushed_object_ids = [123, 12]
        expected_scene.add_entity(expected_pushable_object1)
        expected_scene.add_entity(expected_pushable_object2)
        expected_scene.add_entity(expected_pusher_object)
        expected_scene.add_entity(expected_dummy_action)

        scene = Scene()
        pushable_object1 = Object(id=123, name="dummy", position=Vector(1, 1), tags=['pushable'])
        pushable_object2 = Object(id=12, name="dummy", position=Vector(1, 1), tags=['pushable'])
        pusher_object = Object(id=456, name="dummy", position=Vector(2, 1))
        dummy_action = Push(object_id=456, direction=Vector(-1, 0))
        dummy_action.pushed_object_ids = [123, 12]
        scene.add_entity(pushable_object1)
        scene.add_entity(pushable_object2)
        scene.add_entity(pusher_object)
        scene.add_entity(dummy_action)
        dummy_action.apply(scene)

        # check if two pushable objects on the square we are pushing have been pushed
        assert expected_pushable_object1 == pushable_object1
        assert expected_pushable_object2 == pushable_object2

        # checks if two pushable objects are on the new square
        assert scene.get_objects_by_position(Vector(0, 1)) == [pushable_object1, pushable_object2]

        # checks if there are no objects left on the square we pushed
        assert scene.get_objects_by_position(Vector(1, 1)) == []
