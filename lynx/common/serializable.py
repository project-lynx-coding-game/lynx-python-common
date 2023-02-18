import json

class Serializable:
    """
    Represents an abstract class which can be converted to `str` and return
    string in format that can be easily deserialized by other microservices.
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        exported_vars = {k: v for k, v in self.__dict__ if not k[0]=='_'}
        return f"{{ \"type\" : \"{self.__class__.__name__}\", " \
               f"\"data\" : {json.dumps(exported_vars, default=str)} }} "
