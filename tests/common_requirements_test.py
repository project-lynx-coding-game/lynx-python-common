from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.square import Square
from lynx.common.vector import Vector


class TestIsWalkable:

    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=True)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert result is True

    @patch('lynx.common.scene.Scene')
    def test_failure(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=False)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert result is False
