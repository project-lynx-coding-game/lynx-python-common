import json
from typing import get_type_hints, get_args


class Serializable:
    """
    Represents an abstract class which can be converted to `str` and return
    string in format that can be easily deserialized by other microservices.
    """

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return self.serialize()

    def serialize(self) -> str:
        exported_vars = {k: v for k,
                         v in self.__dict__.items() if not k.startswith("_")}
        # The `lambda` converts strings such as `{}` into objects such as {},
        # so we do not end up with nested strings with complex objects
        return f"{json.dumps(exported_vars, default=lambda x: json.loads(x.serialize()))}"

    # This method is responsible for populating instance of an object
    # with data from `JSON`. Usually, `self` contains defaultly initialized
    # instance of the class
    def populate(self, json_string) -> None:
        json_data = json.loads(json_string)
        for exported_var in json_data.keys():
            # If deserialized object is a list
            if type(self.__dict__[exported_var]) == list:
                # Here we fetch the `inner`` type of List[>inner<]
                element_type = get_args(get_type_hints(self).get(exported_var))[0]

                # Now we walk through all jsons, if the type is simple
                # we just append value from json. Else, we call `deserialize`
                if element_type in (int, float, bool, str):
                    for serialized_element in json_data[exported_var]:
                        self.__dict__[exported_var].append(serialized_element)
                else:
                    for serialized_element in json_data[exported_var]:
                        self.__dict__[exported_var].append(
                            element_type.deserialize(json.dumps(serialized_element)))
            # If object we are deserializing is primitive
            elif not hasattr(self.__dict__[exported_var], '__dict__'):
                self.__dict__[exported_var] = json_data[exported_var]
            # Deserialzied object is a class
            else:
                variable_type = type(self.__dict__[exported_var])
                self.__dict__[exported_var] = variable_type.deserialize(
                    json.dumps(json_data[exported_var]))

    @classmethod
    def deserialize(cls, json_string: str):  # TODO: returning `Self` was not working
        # All serializable classes must have parameterless constructor
        instance = cls()
        instance.populate(json_string)
        return instance
