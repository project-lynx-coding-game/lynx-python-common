from typing import NoReturn

from lynx.common.actions.move import Move
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


def test_scene_deserialization_success() -> NoReturn:
    expected_scene = Scene()
    dummy_object = Object(id=123, name="dummy", position=Vector(0, 0))
    dummy_action = Move(object_id=456, vector=Vector(1, 1))
    expected_scene.add_entity(dummy_object)
    expected_scene.add_entity(dummy_action)
    serialized_expected_scene = expected_scene.serialize()

    deserialzied_scene = Scene.deserialize(serialized_expected_scene)

    assert deserialzied_scene == expected_scene
