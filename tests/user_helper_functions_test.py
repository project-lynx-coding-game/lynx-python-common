import random
from typing import NoReturn

from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector
from lynx.common.actions.user_helper_functions import get_objects_around, get_position, can_i_stand, get_type, calculate_distance_to, filter_objects, random_direction


class TestUserHelperFunctions:
    scene = Scene()
    dummy_agent = Object(id=1, name="agent", position=Vector(0, 0))
    scene.add_entity(dummy_agent)
    dummy_object1 = Object(id=2, name="dummy", position=Vector(5, 5), tags=["tile"])
    scene.add_entity(dummy_object1)
    dummy_object2 = Object(id=3, name="dummy", position=Vector(3, 5))
    scene.add_entity(dummy_object2)
    dummy_object3 = Object(id=4, name="diff_dummy", position=Vector(1, 1))
    scene.add_entity(dummy_object3)

    def test_objects_around_success(self) -> NoReturn:
        assert get_objects_around(1, self.scene, 9) == [3, 4]

    def test_objects_around_failure(self) -> NoReturn:
        assert get_objects_around(1, self.scene, 7) != [3, 4]

    def test_get_position_success(self) -> NoReturn:
        assert get_position(self.scene, 3) == Vector(3, 5)

    def test_can_i_stand_success(self) -> NoReturn:
        assert can_i_stand(self.scene, Vector(5, 5)) is True

    def test_can_i_stand_failure(self) -> NoReturn:
        assert can_i_stand(self.scene, Vector(3, 5)) is False

    def test_get_type_success(self) -> NoReturn:
        assert get_type(self.scene, 1) == "agent"

    def test_get_type_failure(self) -> NoReturn:
        assert get_type(self.scene, 2) != "agent"

    def test_distance_to_success(self) -> NoReturn:
        assert calculate_distance_to(self.scene, 4, 1) == 2

    def test_filter_objects_success(self) -> NoReturn:
        assert filter_objects(self.scene, [1, 2, 3, 4], "dummy") == [2, 3]

    def test_filter_objects_failure(self) -> NoReturn:
        assert filter_objects(self.scene, [1, 2, 3, 4], "empty") != [1]

    def test_random_direction_success(self) -> NoReturn:
        random.seed(12)
        self.scene.add_entity(Object(id=10, name="Grass", position=Vector(-1, 0), tags=["tile"]))
        self.scene.add_entity(Object(id=11, name="Grass", position=Vector(0, 1), tags=["tile"]))
        assert random_direction(self.scene, 1) == Vector(-1, 0)

    def test_random_direction_failure(self) -> NoReturn:
        assert random_direction(self.scene, 1) != Vector(1, 0)
