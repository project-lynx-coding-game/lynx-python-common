import json
from typing import NoReturn

from lynx.common.actions.move import Move
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


class TestSceneSerialization:
    expected_serialized_scene = '{"players": [], "entities": [{"type": "Object", "attributes": {"id": 123, "name": "dummy", ' \
                                '"position": {"x": 0, "y": 0}, "additional_positions": [], "state": "", ' \
                                '"tick": "", "on_death": "", "owner": "", "tags": [], "inventory": {}}}, ' \
                                '{"type": "Move", "attributes": {"object_id": 456, "direction": {"x": 1, "y": ' \
                                '0}}}], "pending_actions": []}'

    def test_success(self) -> NoReturn:
        scene = Scene()

        dummy_object = Object(id=123, name="dummy", position=Vector(0, 0))
        dummy_action = Move(object_id=456, direction=Vector(1, 0))
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_action)
        serialized_scene = scene.serialize()

        assert serialized_scene == self.expected_serialized_scene

    def test_failure(self) -> NoReturn:
        scene = Scene()
        dummy_object = Object(id=789, name="dummy", position=Vector(0, 0))
        dummy_action = Move(object_id=1011, direction=Vector(1, 0))
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_action)
        serialized_scene = scene.serialize()

        assert serialized_scene != self.expected_serialized_scene


class TestSceneDeserialization:
    expected_deserialized_scene = Scene()
    dummy_object = Object(id=123, name="dummy", position=Vector(0, 0))
    dummy_action = Move(object_id=456, direction=Vector(1, 0))
    expected_deserialized_scene.add_entity(dummy_object)
    expected_deserialized_scene.add_entity(dummy_action)

    def test_success(self) -> NoReturn:
        serialized_scene = '{"players": [], "entities": [{"type": "Object", "attributes": {"id": 123, "name": "dummy", "position": {"x": 0, "y": 0}, ' \
                           '"additional_positions": [], "state": "", "tick": "", "on_death": "", "owner": "", "tags": []}}, {"type": "Move", ' \
                           '"attributes": {"object_id": 456, "direction": {"x": 1, "y": 0}}}]} '
        deserialzied_scene = Scene.deserialize(json.loads(serialized_scene))

        assert deserialzied_scene == self.expected_deserialized_scene

    def test_failure(self) -> NoReturn:
        serialized_scene = '{ "players": [], "entities": [{"type": "Object", "attributes": {"id": 789, "name": "dummy", "position": {"x": 0, "y": 0}, ' \
                           '"additional_positions": [], "state": "", "tick": "", "on_death": "", "owner": "", "tags": []}}, {"type": "Move", ' \
                           '"attributes": {"object_id": 1011, "direction": {"x": 1, "y": 0}}}]} '
        deserialzied_scene = Scene.deserialize(json.loads(serialized_scene))

        assert deserialzied_scene != self.expected_deserialized_scene
