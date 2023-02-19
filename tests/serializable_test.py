from dataclasses import dataclass
import pytest
import sys, os

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
    assert log == '{"exported_field": "DO_EXPORT_THAT+++", "complex_field": {\"nested_field\": \"THIS_SHOULD_BE_NESTED+++\"}}'


    deserialized = TestClass.deserialize(log)
    assert deserialized == test_object

