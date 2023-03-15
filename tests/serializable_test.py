from dataclasses import dataclass, field
from typing import List

from lynx.common.serializable import Serializable


@dataclass
class OtherDummy(Serializable):
    nested_field: str = "THIS_SHOULD_BE_NESTED"


class Dummy(Serializable):
    def __init__(self) -> None:
        super().__init__()
        self.exported_field = "DO_EXPORT_THAT"
        self.complex_field = OtherDummy()
        self._private_field = "DO_!NOT!_EXPORT"

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return False
        return (self.exported_field, self.complex_field) == (__o.exported_field, __o.complex_field)


class TestSerializableSerialization:
    expected_serialized_test_object = '{"exported_field": "DO_EXPORT_THAT+++", "complex_field": {\"nested_field\": \"THIS_SHOULD_BE_NESTED+++\"}}'

    def test_success(self):
        test_object = Dummy()
        test_object.exported_field += "+++"
        test_object.complex_field.nested_field += "+++"
        serialized_test_object = test_object.serialize()

        assert serialized_test_object == self.expected_serialized_test_object

    def test_failure(self):
        test_object = Dummy()
        test_object.exported_field += "---"
        test_object.complex_field.nested_field += "---"
        serialized_test_object = test_object.serialize()

        assert serialized_test_object != self.expected_serialized_test_object


class TestSerializableDeserialization:
    expected_deserialized_test_object = Dummy()
    expected_deserialized_test_object.exported_field += "+++"
    expected_deserialized_test_object.complex_field.nested_field += "+++"

    def test_success(self):
        serialized_test_object = '{"exported_field": "DO_EXPORT_THAT+++", "complex_field": {\"nested_field\": \"THIS_SHOULD_BE_NESTED+++\"}}'
        deserialized_test_object = Dummy.deserialize(serialized_test_object)

        assert deserialized_test_object == self.expected_deserialized_test_object

    def test_failure(self):
        serialized_test_object = '{"exported_field": "DO_EXPORT_THAT---", "complex_field": {\"nested_field\": \"THIS_SHOULD_BE_NESTED---\"}}'
        deserialized_test_object = Dummy.deserialize(serialized_test_object)

        assert deserialized_test_object != self.expected_deserialized_test_object


@dataclass
class DummyListElement(Serializable):
    number: int = 0


@dataclass
class DummyList(Serializable):
    list: List[DummyListElement] = field(default_factory=list)


class TestSerializableListSerialization:
    expected_serialized_test_list = '{"list": [{"number": 1}, {"number": 2}, {"number": 3}]}'

    def test_success(self):
        test_list = DummyList(list=[DummyListElement(1), DummyListElement(2), DummyListElement(3)])
        serialized_test_list = test_list.serialize()

        assert serialized_test_list == self.expected_serialized_test_list

    def test_failure(self):
        test_list = DummyList(list=[DummyListElement(4), DummyListElement(5), DummyListElement(6)])
        serialized_test_list = test_list.serialize()

        assert serialized_test_list != self.expected_serialized_test_list


class TestSerializableListDeserialization:
    expected_deserialized_test_list = DummyList(list=[DummyListElement(1), DummyListElement(2), DummyListElement(3)])

    def test_success(self):
        serialized_test_list = '{"list": [{"number": 1}, {"number": 2}, {"number": 3}]}'
        deserialized_test_list = DummyList.deserialize(serialized_test_list)

        assert deserialized_test_list == self.expected_deserialized_test_list

    def test_failure(self):
        serialized_test_list = '{"list": [{"number": 4}, {"number": 5}, {"number": 6}]}'
        deserialized_test_list = DummyList.deserialize(serialized_test_list)

        assert deserialized_test_list != self.expected_deserialized_test_list


def test_serializable_constructors_success():
    # we import every `Serializable` type, to check if they have parameterless constructors
    # TODO: simplify following imports
    from lynx.common.scene import Scene
    from lynx.common.object import Object
    from lynx.common.actions.move import Move
    Scene()
    Object()
    Move()
