from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.vector import Vector


class TestIsWalkable:

    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene) -> NoReturn:
        mock_object_at_destination = MagicMock(
            walkable=True
        )
        mock_scene.get_object_by_position.return_value = mock_object_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert result is True

    @patch('lynx.common.scene.Scene')
    def test_failure(self, mock_scene) -> NoReturn:
        mock_scene.get_object_by_position.return_value = None

        result: bool = CommonRequirements.is_walkable(mock_scene, 1, Vector(1, 0))

        assert result is False
