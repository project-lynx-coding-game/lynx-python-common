from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.square import Square
from lynx.common.vector import Vector
from lynx.common.object import Object
from lynx.common.scene import Scene


class TestIsWalkable:

    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=True)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert result

    @patch('lynx.common.scene.Scene')
    def test_failure(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=False)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert not result


class TestIsPushable:
    def test_success(self) -> NoReturn:
        scene = Scene()
        dummy_object1 = Object(id=123, name="dummy", position=Vector(0, 0), pushable=False)
        dummy_object2 = Object(id=456, name="dummy", position=Vector(0, 0), pushable=True)
        scene.add_entity(dummy_object1)
        scene.add_entity(dummy_object2)

        assert CommonRequirements.is_pushable(scene, Vector(0, 0))

    def test_failure(self) -> NoReturn:
        scene = Scene()
        dummy_object = Object(id=123, name="dummy", position=Vector(0, 0), pushable=False)
        scene.add_entity(dummy_object)

        assert not CommonRequirements.is_pushable(scene, Vector(0, 0))
