from typing import List

from lynx.python.common.point import Point
from lynx.python.common.enums import Direction
from lynx.python.common.serializable import Serializable, Properties


class Object(Serializable):
    """
    Abstract object existing in a `scene`. Represents part of scene's state,
    in contrast to `Action` which represents only modifications of the state.
    """
    base: str
    properties: Properties
    scene: 'Scene'
    walkable: bool

    def __init__(self, position: Point, scene: 'Scene') -> None:
        super().__init__(__class__.__name__)
        self.properties.id = scene.last_object_id  # int
        self.properties.position = position  # Point
        self.scene = scene
        self.walkable = False

        scene.add_object_to_position_map(self, position)
        scene.add_object_to_id_map(self)
        scene.increment_last_object_id()

        # Log creation of the `Object`
        print(self)

    def occupied_fields(self, current_position: Point = None) -> List[Point]:
        if not current_position:
            current_position = self.properties.position
        return [current_position]

    def fields_around(self) -> List[Point]:
        fields = []
        for field in self.occupied_fields():
            points_around_field = [field + Direction.NORTH.value,
                                   field + Direction.WEST.value,
                                   field + Direction.SOUTH.value,
                                   field + Direction.EAST.value]
            # append all points around that aren't in self.occupied_fields()
            fields.extend(list(filter(lambda point: point not in self.occupied_fields(), points_around_field)))
        return fields

    def tick(self) -> None:
        """
        Called every turn of the object to perform actions
        """

    def on_collision(self, other) -> None:
        """
        This method is called when other `Object` enters
        the `field` this object is on.
        """
