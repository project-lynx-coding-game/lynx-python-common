import pytest
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector


def test_scene_serialization():
    scene = Scene()
    test_object = Object(id=3123, name="generic guy", position=Vector(5,321))
    scene.add_object(test_object)
    
    serialized_scene = scene.serialize()

    deserialzied_scene = Scene.deserialize(serialized_scene)

    assert scene == deserialzied_scene