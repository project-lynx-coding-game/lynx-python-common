import json


class Properties:
    """
    Properties is an empty class
    used by objects inheriting from Serialzable
    to store variables that will be serialized
    """

    def __init__(self) -> None:
        pass


class Serializable:
    """
    Represents an abstract class which can be converted to `str` and return
    string in format that can be easily deserialized by various frontends.
    """
    base: str
    properties: Properties

    def __init__(self, base: str) -> None:
        self.base = base
        self.properties = Properties()

    def __str__(self) -> str:
        return f"{{ \"base_class_name\" : \"{self.base}\", \"class_name\" : \"{self.__class__.__name__}\", " \
               f"\"properties\" : {json.dumps(self.properties.__dict__, default=str)} }} "
