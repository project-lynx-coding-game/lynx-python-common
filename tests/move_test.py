from typing import NoReturn

from lynx.common.actions.move import Move
from lynx.common.enums import Direction


class TestMoveSerialization:
    expected_serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 123, \\"vector\\": {\\"x\\": 0, \\"y\\": 1}}"}'

    def test_success(self) -> NoReturn:

        serialized_move = Move(object_id=123, vector=Direction.NORTH.value).serialize()
        assert serialized_move == self.expected_serialized_move

    def test_failure(self) -> NoReturn:
        serialized_move = Move(object_id=345, vector=Direction.WEST.value).serialize()
        assert serialized_move != self.expected_serialized_move


class TestMoveDeserialization:
    expected_deserialized_move = Move(object_id=123, vector=Direction.NORTH.value)

    def test_success(self) -> NoReturn:
        serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 123, \\"vector\\": {\\"x\\": 0, \\"y\\": 1}}"}'
        deserialized_move = Move.deserialize(serialized_move)

        assert deserialized_move == self.expected_deserialized_move

    def test_failure(self) -> NoReturn:
        serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 345, \\"vector\\": {\\"x\\": 1, \\"y\\": 2}}"}'
        deserialized_move = Move.deserialize(serialized_move)

        assert deserialized_move != self.expected_deserialized_move
