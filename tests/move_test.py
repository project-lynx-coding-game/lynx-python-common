from typing import NoReturn

from lynx.common.actions.move import Move
from lynx.common.enums import Direction


def test_move_serialization_success() -> NoReturn:
    expected_serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 123, \\"vector\\": {\\"x\\": 0, \\"y\\": 1}}"}'
    serialized_move = Move(object_id=123, vector=Direction.NORTH.value).serialize()
    assert serialized_move == expected_serialized_move


def test_move_deserialization_success() -> NoReturn:
    expected_deserialized_move = Move(object_id=123, vector=Direction.NORTH.value)

    serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 123, \\"vector\\": {\\"x\\": 0, \\"y\\": 1}}"}'
    deserialized_move = Move.deserialize(serialized_move)

    assert deserialized_move == expected_deserialized_move


def test_move_deserialization_failure() -> NoReturn:
    expected_deserialized_move = Move(object_id=123, vector=Direction.NORTH.value)

    serialized_move = '{"type": "Move", "attributes": "{\\"object_id\\": 345, \\"vector\\": {\\"x\\": 1, \\"y\\": 2}}"}'
    deserialized_move = Move.deserialize(serialized_move)

    assert deserialized_move != expected_deserialized_move
