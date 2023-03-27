import unittest
from typing import NoReturn, Callable
from unittest.mock import patch, MagicMock

from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.vector import Vector


class TestIsWalkableDestination(unittest.TestCase):

    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene) -> NoReturn:
        mock_object_at_destination = MagicMock(
            walkable=True
        )
        mock_scene.get_object_by_position.return_value = mock_object_at_destination

        requirement: Callable = CommonRequirements.is_walkable_destination(1, Vector(1, 0))
        result = requirement(mock_scene)

        self.assertTrue(result)

    @patch('lynx.common.scene.Scene')
    def test_failure(self, mock_scene) -> NoReturn:
        mock_scene.get_object_by_position.return_value = None

        requirement: Callable = CommonRequirements.is_walkable_destination(1, Vector(1, 0))
        result = requirement(mock_scene)

        self.assertFalse(result)
