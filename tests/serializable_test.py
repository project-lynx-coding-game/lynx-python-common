import pytest
import sys
sys.path.append("..")

from lynx.common import Serializable

def test_serializable():
    class TestClass(Serializable):
        def __init__(self) -> None:
            super().__init__()
            self.exported_field = "DO EXPORT THAT"
            self._private_field = "DO NOT EXPORT"

    test_object = TestClass()
    log = str(test_object)
    assert log, "{}"