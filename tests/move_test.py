import json
from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.move import Move
from lynx.common.enums import Direction
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.square import Square
from lynx.common.vector import Vector


class TestMoveSerialization:
    expected_serialized_move = '{"type": "Move", "attributes": {"object_id": 123, "direction": {"x": 0, "y": -1}}}'

    def test_success(self) -> NoReturn:
        serialized_move = Move(
            object_id=123, direction=Direction.NORTH.value).serialize()
        assert serialized_move == self.expected_serialized_move

    def test_failure(self) -> NoReturn:
        serialized_move = Move(
            object_id=345, direction=Direction.WEST.value).serialize()
        assert serialized_move != self.expected_serialized_move


class TestMoveDeserialization:
    expected_deserialized_move = Move(
        object_id=123, direction=Direction.NORTH.value)

    def test_success(self) -> NoReturn:
        serialized_move = '{"type": "Move", "attributes": {"object_id": 123, "direction": {"x": 0, "y": -1}}}'
        deserialized_move = Move.deserialize(json.loads(serialized_move))

        assert deserialized_move == self.expected_deserialized_move

    def test_failure(self) -> NoReturn:
        serialized_move = '{"type": "Move", "attributes": {"object_id": 123, "direction": {"x": 1, "y": 2}}}'
        deserialized_move = Move.deserialize(json.loads(serialized_move))

        assert deserialized_move != self.expected_deserialized_move


class TestMoveRequirements:
    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene):
        dummy_action = Move(
            object_id=123,
            direction=Vector(1, 0)
        )
        walkable_square = Square()
        walkable_square.walkable = MagicMock(return_value=True)
        mock_scene.get_square.return_value = walkable_square

        result: bool = dummy_action.satisfies_requirements(mock_scene)

        assert result is True


class TestMoveApply:
    def test_apply(self) -> NoReturn:
        expected_scene = Scene()
        expected_dummy_object = Object(
            id=123, name="dummy", position=Vector(1, 1))
        expected_dummy_action = Move(object_id=123, direction=Vector(1, 0))
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_action)

        scene = Scene()
        dummy_object = Object(id=123, name="dummy", position=Vector(0, 1))
        dummy_action = Move(object_id=123, direction=Vector(1, 0))
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_action)
        dummy_action.apply(scene)

        assert expected_dummy_object == dummy_object
        assert scene.get_objects_by_position(Vector(1, 1)) == [dummy_object]
        assert scene.get_objects_by_position(Vector(0, 0)) == []
