import random
from typing import List

from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.vector import Vector
from lynx.common.actions.user_helper_functions import objects_around, get_position, can_i_stand, get_type, distance_to, fillter_objects, random_direction


class TestUserHelperFunctions:
    scene = Scene()
    dummy_agent = Object(id=1, name="agent", position=Vector(0, 0))
    scene.add_entity(dummy_agent)
    dummy_object1 = Object(id=2, name="dummy", position=Vector(5, 5), tags=['walkable'])
    scene.add_entity(dummy_object1)
    dummy_object2 = Object(id=3, name="dummy", position=Vector(3, 5))
    scene.add_entity(dummy_object2)
    dummy_object3 = Object(id=4, name="diff_dummy", position=Vector(1, 1))
    scene.add_entity(dummy_object3)

    def test_objects_around_success(self):
        expected_result = [3, 4]

        assert expected_result == objects_around(1, self.scene, 9)

    def test_objects_around_failure(self):
        expected_result = [3, 4]

        assert expected_result != objects_around(1, self.scene, 7)

    def test_get_position_success(self):
        position: Vector = Vector(3, 5)

        assert position == get_position(self.scene, 3)

    def test_can_i_stand_success(self):
        position: bool = True

        assert position == can_i_stand(self.scene, Vector(5, 5))

    def test_can_i_stand_failure(self):
        position: bool = False

        assert position == can_i_stand(self.scene, Vector(3, 5))


    def test_get_type_success(self):
        name_type: str = 'agent'

        assert name_type == get_type(self.scene, 1)

    def test_get_type_failure(self):
        name_type: str = 'agent'

        assert name_type != get_type(self.scene, 2)

    def test_distance_to_success(self):
        distance: float = 2

        assert distance == distance_to(self.scene, 4, 1)

    def test_fillter_objects_success(self):
        selected_ids: List[int] = [2, 3]

        assert selected_ids == fillter_objects(self.scene, [1,2,3,4], 'dummy')

    def test_fillter_objects_failure(self):
        selected_ids: List[int] = [1]

        assert selected_ids != fillter_objects(self.scene, [1, 2, 3, 4], 'empty')


    def test_random_direction_success(self):
        random.seed(12)
        expected_direction: Vector = Vector(-1, 0)

        self.scene.add_entity(Object(id=10, name="Grass",
                                      position=Vector(-1, 0), tags=['walkable']))

        self.scene.add_entity(Object(id=11, name="Grass",
                                      position=Vector(0, 1), tags=['walkable']))
        assert expected_direction == random_direction(self.scene, 1)

    def test_random_direction_failure(self):
        random.seed(12)
        expected_direction: Vector = Vector(1, 0)

        assert expected_direction != random_direction(self.scene, 1)
