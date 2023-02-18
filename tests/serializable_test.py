import pytest
import sys, os

from lynx.common.serializable import Serializable

def test_serializable():
    class TestClass(Serializable):
        def __init__(self) -> None:
            super().__init__()
            self.exported_field = "DO_EXPORT_THAT"
            self._private_field = "DO_!NOT!_EXPORT"

    test_object = TestClass()
    log = str(test_object)
    assert log == '{"type": "TestClass", "data": {"exported_field": "DO_EXPORT_THAT"}}'