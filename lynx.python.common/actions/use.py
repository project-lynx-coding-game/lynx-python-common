from lynx.python.common.actions.action import Action
from lynx.python.common.point import Point
from lynx.python.common.serializable import Properties
from lynx.python.common.objects.interactive_object import InteractiveObject
from lynx.python.common.objects.object import Object


class Use(Action):
    """
    An action that provides the opportunity to interact with another object
    """
    base: str
    properties: Properties
    triggering_object: Object
    object_id: int  # object id for interaction
    action: str  # name of the action method to call
    range: int

    def __init__(self, triggering_object: Object, object_id: int, action: str, range: int = 1) -> None:
        super().__init__()
        self.properties.triggering_object = triggering_object
        self.properties.object_id = object_id
        self.action = action
        self.range = range

    def execute(self) -> None:
        object_to_interact = self.triggering_object.scene.objects_dict.get(self.object_id)
        if not self.__can_interact(object_to_interact):
            # log here
            return
        self.__call_action(object_to_interact)

    def __call_action(self, object_to_interact):
        getattr(object_to_interact, self.action)()

    def __can_interact(self, object_to_interact: InteractiveObject):
        if not issubclass(object_to_interact.__class__, InteractiveObject):
            return False

        object_position = self.triggering_object.properties.position
        interactive_object_position = object_to_interact.properties.position
        for i in range(-self.range, self.range + 1):
            for j in range(-self.range, self.range + 1):
                if interactive_object_position.__eq__(object_position.__add__(Point(i, j))):
                    return True

        return False
