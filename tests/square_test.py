import pytest

from lynx.common.object import Object
from lynx.common.square import Square


class TestSquareAppend:
    def test_object_success(self):
        object = Object(name="Ondrej")
        square = Square()
        square.append(object)

        assert square.objects == [object]
        assert square.ground is None

    def test_ground_success(self):
        object = Object(name="Ondrej", tags=['walkable'])
        square = Square()
        square.append(object)

        assert square.objects == [object]
        assert square.ground == object

    def test_object_ground_success(self):
        object = Object(name="Ondrej")
        ground = Object(name="Groundriej", tags=['walkable'])
        square = Square()
        square.append(object)
        square.append(ground)

        assert square.objects == [object, ground]
        assert square.ground == ground

    def test_ground_failure(self):
        object = Object(name="Ondrej", tags=['walkable'])
        ground = Object(name="Groundriej", tags=['walkable'])
        square = Square()
        square.append(object)

        with pytest.raises(Exception):
            square.append(ground)


class TestSquareRemove:
    def test_object_success(self):
        object = Object(name="Ondrej")
        square = Square()
        square.append(object)
        square.remove(object)

        assert square.objects == []
        assert square.ground is None

    def test_ground_success(self):
        object = Object(name="Ondrej")
        ground = Object(name="Groundriej", tags=['walkable'])
        square = Square()
        square.append(object)
        square.append(ground)
        square.remove(ground)

        assert square.objects == [object]
        assert square.ground is None

    def test_ground_failure(self):
        object = Object(name="Ondrej")
        object2 = Object(name="Undriej")
        square = Square()
        square.append(object)

        with pytest.raises(ValueError):
            square.remove(object2)
