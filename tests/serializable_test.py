from dataclasses import dataclass, field
from typing import List

from lynx.common.serializable import Serializable

def test_serializable():
    @dataclass
    class OtherTestClass(Serializable):
        nested_field: str = "THIS_SHOULD_BE_NESTED"

    class TestClass(Serializable):
        def __init__(self) -> None:
            super().__init__()
            self.exported_field = "DO_EXPORT_THAT"
            self.complex_field = OtherTestClass()
            self._private_field = "DO_!NOT!_EXPORT"
            
        def __eq__(self, __o: object) -> bool:
            if not isinstance(__o, self.__class__):
                return False
            return (self.exported_field, self.complex_field) ==(__o.exported_field, __o.complex_field)

    test_object = TestClass()
    test_object.exported_field += "+++"
    test_object.complex_field.nested_field += "+++"
    log = test_object.serialize()

    # The serialized object should comply to the following format:
    assert log == '{"exported_field": "DO_EXPORT_THAT+++", "complex_field": {\"nested_field\": \"THIS_SHOULD_BE_NESTED+++\"}}'


    # Deserialization should result in `equal` object
    deserialized = TestClass.deserialize(log)
    assert deserialized == test_object

def test_serializable_list():
    @dataclass
    class TestClass(Serializable):
        number: int = 0

    @dataclass
    class TestListClass(Serializable):
        list: List[TestClass] = field(default_factory=list)

    list_instance = TestListClass(list=[TestClass(1), TestClass(2), TestClass(3)])
    list_instance_serialized = list_instance.serialize()

    assert list_instance_serialized == '{"list": [{"number": 1}, {"number": 2}, {"number": 3}]}'
    list_instance_deserialized = TestListClass.deserialize(list_instance_serialized)

    assert list_instance == list_instance_deserialized

def test_serializable_constructors():
    # TODO: test which would walk over all classes, check if they
    # inherit from `Serializable`. If so, they should have a
    # parameterless constructor

    #import lynx.common.serializable as common_object
    #classes = inspect.getmembers(common_object, inspect.isclass)
    #print(classes)
    pass
