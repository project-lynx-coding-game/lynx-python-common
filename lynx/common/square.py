from dataclasses import dataclass, field
from typing import List, Optional

from lynx.common.object import Object


# class wrapping logic of a tile and objects placed on it
@dataclass
class Square:
    tile_object: Optional[Object] = None
    objects: List[Object] = field(default_factory=list)

    def append(self, object: Object) -> None:
        if object.has_tags(['tile']) and self.tile_object is not None:
            # TODO: in the future when we add logger we should log this event
            raise Exception("Cannot put more than one tile in a square!")

        if object.has_tags(['tile']):
            self.tile_object = object

        self.objects.append(object)

    def remove(self, object: Object) -> None:
        if self.tile_object == object:
            self.tile_object = None

        self.objects.remove(object)

    def tile(self) -> bool:
        objects_tags = [object_on_tile.tags for object_on_tile in self.objects]
        contains_tile = True

        for object_tags in objects_tags:
            if 'tile' not in object_tags:
                contains_tile = False

        return self.tile_object is not None and contains_tile
