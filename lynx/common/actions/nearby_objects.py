from lynx.common.actions.action import Action
from lynx.common.point import Point
from lynx.common.serializable import Properties
from lynx.common.objects.interactive_object import InteractiveObject
from lynx.common.objects.object import Object


class NearbyObjects(Action):
    """
    Action to retrieve nearby objects within the range of the triggering object
    """
    base: str
    properties: Properties
    object: Object
    range: int

    def __init__(self, object: Object, range: int = 1) -> None:
        super().__init__()
        self.properties.object_id = object.properties.id
        self.object = object
        self.range = range

    def execute(self) -> None:
        self.properties.nearby_objects = self.__get_nearby_objects()
        # should be changed to a log as list containing nearby items
        self.log()

    def __get_nearby_objects(self):
        nearby_objects = []
        for i in range(-self.range, self.range + 1):
            for j in range(-self.range, self.range + 1):
                objects_on_field = self.object.scene.get_objects_by_position(
                    self.object.properties.position.__add__(Point(i, j)))
                if objects_on_field is None:
                    continue

                nearby_objects.extend(list(
                    filter(lambda nearby_object: (isinstance(nearby_object, InteractiveObject)), objects_on_field)))
        return list(map(lambda x: (
            {
                'class_name': x.__class__.__name__,
                'id': x.properties.id,
                'position': x.properties.position
            }
        ), nearby_objects))
