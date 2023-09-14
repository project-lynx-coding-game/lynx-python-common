import random
from typing import NoReturn

from lynx.common.actions.action import Action
from lynx.common.actions.drop import Drop
from lynx.common.object import Object
from lynx.common.player import Player
from lynx.common.scene import Scene
from lynx.common.vector import Vector
from lynx.common.actions.update_resources import UpdateResources

class TestDropSerialization:
    expected_serialization_drop = '{"type": "Drop", "attributes": {"object_id": 1, "target_position": {"x": 1, "y": 0}}}'

    def test_success_serialization(self) -> None:
        serialized_drop = Drop(object_id=1, target_position=Vector(1, 0)).serialize()

        assert self.expected_serialization_drop == serialized_drop

    def test_success_deserialization(self) -> None:
        expected_drop = Drop(object_id=1, target_position=Vector(1, 0))
        dummy_drop = Drop.deserialize(self.expected_serialization_drop)

        assert dummy_drop == expected_drop


class TestDropApply:
    def test_drop_single_object_in_overworld_on_tile_sucessful(self) -> None:
        random.seed(1222)
        expected_scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        expected_dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5))
        expected_dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_drop)
        expected_scene.add_entity(expected_dummy_object2)

        random.seed(1222)
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_drop)

        dummy_drop.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene

    def test_drop_multiple_objects_in_overworld_on_tile_sucessful(self) -> None:
        random.seed(1222)
        expected_scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        expected_dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5))
        expected_dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        expected_dummy_object2 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_dummy_object3 = Object(id=expected_scene.generate_id(), name="Wood", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_dummy_object4 = Object(id=expected_scene.generate_id(), name="Stone", position=Vector(5, 6),
                                        tags=['pushable', 'pickable'])
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_drop)
        expected_scene.add_entity(expected_dummy_object2)
        expected_scene.add_entity(expected_dummy_object3)
        expected_scene.add_entity(expected_dummy_object4)

        random.seed(1222)
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5), inventory={"Wood": 2, "Stone": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_drop)

        dummy_drop.apply(scene)
        for action in scene.pending_actions:
            Action.deserialize(action).apply(scene)
        scene.pending_actions.clear()

        assert scene == expected_scene

    def test_success_drop_to_drop_area_apply(self) -> None:
        expected_scene = Scene(players=[Player(player_id="test", player_resources={"Wood": 2, "Stone": 1}, drop_area=Vector(5, 6))])
        expected_dummy_object = Object(id=1, name="dummy", owner="test", position=Vector(5, 5))
        expected_dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        expected_update_points = UpdateResources(user_name="test", points_updated = {"Wood": 2, "Stone": 1})
        expected_scene.add_entity(expected_dummy_object)
        expected_scene.add_entity(expected_dummy_drop)
        expected_scene.pending_actions.append(expected_update_points.serialize())

        scene = Scene(players=[Player(player_id="test", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 6))])
        dummy_object = Object(id=1, name="dummy", owner="test", position=Vector(5, 5), inventory={"Wood": 2, "Stone": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(dummy_object)
        scene.add_entity(dummy_drop)

        dummy_drop.apply(scene)

        assert scene == expected_scene


class TestDropRequirements:

    def test_all_requirements_satisified_positive(self) -> None:
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is True

    def test_requirements_agent_too_far_fail(self) -> None:
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(6, 6), object_id=1)
        scene.add_entity(Object(id=3, name="Grass", position=Vector(6, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True

    def test_requirements_empty_inventory_fail(self) -> None:
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5))
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6), tags=['walkable']))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True

    def test_requirements_no_walkable_tile_fail(self) -> None:
        scene = Scene(players=[Player(player_id="dummy", player_resources={"Wood": 0, "Stone": 0}, drop_area=Vector(5, 5))])
        dummy_object = Object(id=1, name="dummy", owner="dummy", position=Vector(5, 5), inventory={"Wood": 1})
        dummy_drop = Drop(target_position=Vector(5, 6), object_id=1)
        scene.add_entity(Object(id=3, name="Grass", position=Vector(5, 6)))
        scene.add_entity(dummy_object)
        assert dummy_drop.satisfies_requirements(scene) is not True
