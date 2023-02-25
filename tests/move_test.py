from lynx.common.actions.move import Move
from lynx.common.enums import Direction


def test_move_serialization():
    move = Move(object_id=123, vector=Direction.NORTH.value)
    serialized_move = move.serialize()

    assert serialized_move == '{"object_id": 123, "vector": {"x": 0, "y": 1}}'

    deserialized_move = Move.deserialize(serialized_move)

    assert deserialized_move == move

def test_move_serialization_fail():
    move = Move(object_id=123, vector=Direction.NORTH.value)
    serialized_move = '{"object_id": 124, "vector": {"x": 0, "y": 1}}'

    deserialized_move = Move.deserialize(serialized_move)

    assert (deserialized_move == move) == False
