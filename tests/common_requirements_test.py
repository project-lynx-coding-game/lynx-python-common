from typing import NoReturn
from unittest.mock import patch, MagicMock

from lynx.common.actions.common_requirements import CommonRequirements
from lynx.common.square import Square
from lynx.common.vector import Vector
from lynx.common.object import Object
from lynx.common.scene import Scene
from lynx.common.enums import Direction


class TestIsWalkable:
    @patch('lynx.common.scene.Scene')
    def test_success(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=True)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, Vector(1, 0))

        assert result

    @patch('lynx.common.scene.Scene')
    def test_failure(self, mock_scene) -> NoReturn:
        mock_square_at_destination = Square()
        mock_square_at_destination.walkable = MagicMock(return_value=False)
        mock_scene.get_square.return_value = mock_square_at_destination

        result: bool = CommonRequirements.is_walkable(mock_scene, Vector(1, 0))

        assert not result


class TestCanBeStacked:
    scene = Scene()
    dummy_object1 = Object(id=123, name="dummy", position=Vector(0, 0))
    scene.add_entity(dummy_object1)

    def test_success(self) -> NoReturn:
        assert CommonRequirements.can_be_stacked(self.scene, Vector(0, 0), "dummy")

    def test_different_object_name_failure(self) -> NoReturn:
        assert not CommonRequirements.can_be_stacked(self.scene, Vector(0, 0), "dummy123")

    def test_no_object_failure(self) -> NoReturn:
        assert not CommonRequirements.can_be_stacked(self.scene, Vector(1, 0), "dummy")


class TestIsProperDirection:
    def test_north_vector_proper(self) -> NoReturn:
        assert CommonRequirements.is_proper_direction(Direction.NORTH.value)

    def test_south_vector_proper(self) -> NoReturn:
        assert CommonRequirements.is_proper_direction(Vector(0, -1))

    def test_huge_vector_improper(self) -> NoReturn:
        assert not CommonRequirements.is_proper_direction(Vector(100, 100))


class TestContainTags:
    scene = Scene()
    dummy_object1 = Object(id=123, name="dummy", position=Vector(0, 0), tags=['walkable', 'pushable'])
    scene.add_entity(dummy_object1)

    def test_has_proper_tag_positive(self) -> NoReturn:
        assert CommonRequirements.has_given_tags(self.scene, 123, ['walkable'])

    def test_has_improper_tag_negative(self) -> NoReturn:
        assert not CommonRequirements.has_given_tags(self.scene, 123, ['insertable'])

    def test_has_proper_tags_positive(self) -> NoReturn:
        assert CommonRequirements.has_given_tags(self.scene, 123, ['walkable', 'pushable'])

    def test_has_improper_tags_negative(self) -> NoReturn:
        assert not CommonRequirements.has_given_tags(self.scene, 123, ['walkable', 'pushable', 'insertable'])

class TestIsAnyOnSquare:
    scene = Scene()
    dummy_object1 = Object(id=123, name="dummy", position=Vector(0, 0))
    scene.add_entity(dummy_object1)
    dummy_object2 = Object(id=1234, name="tree", position=Vector(0, 0))
    scene.add_entity(dummy_object2)

    def test_existing_tree_on_square_positive(self) -> NoReturn:
        assert CommonRequirements.is_any_on_square(self.scene, Vector(0, 0), ['tree'])

    def test_nonexistent_object_on_square_negative(self) -> NoReturn:
        assert not CommonRequirements.is_any_on_square(self.scene, Vector(0, 0), ['test'])
