import pytest

from lynx.common.object import Object
from lynx.common.square import Square


class TestSquareAppend:
    def test_object_success(self):
        object = Object(name="Ondrej")
        square = Square()
        square.append(object)

        assert square.objects == [object]
        assert square.tile_object is None

    def test_tile_object_success(self):
        object = Object(name="Ondrej", tags=['tile'])
        square = Square()
        square.append(object)

        assert square.objects == [object]
        assert square.tile_object == object

    def test_object_and_tile_object_success(self):
        object = Object(name="Ondrej")
        tile_object = Object(name="tile_objectriej", tags=['tile'])
        square = Square()
        square.append(object)
        square.append(tile_object)

        assert square.objects == [object, tile_object]
        assert square.tile_object == tile_object

    def test_tile_object_failure(self):
        object = Object(name="Ondrej", tags=['tile'])
        tile_object = Object(name="tile_objectriej", tags=['tile'])
        square = Square()
        square.append(object)

        with pytest.raises(Exception):
            square.append(tile_object)


class TestSquareRemove:
    def test_object_success(self):
        object = Object(name="Ondrej")
        square = Square()
        square.append(object)
        square.remove(object)

        assert square.objects == []
        assert square.tile_object is None

    def test_tile_object_success(self):
        object = Object(name="Ondrej")
        tile_object = Object(name="tile_objectriej", tags=['tile'])
        square = Square()
        square.append(object)
        square.append(tile_object)
        square.remove(tile_object)

        assert square.objects == [object]
        assert square.tile_object is None

    def test_tile_object_failure(self):
        object = Object(name="Ondrej")
        object2 = Object(name="Undriej")
        square = Square()
        square.append(object)

        with pytest.raises(ValueError):
            square.remove(object2)
