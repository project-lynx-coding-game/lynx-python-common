
from dataclasses import dataclass, field
from typing import List, NoReturn

from lynx.common.object import Object

# Class wraping logic of ground and objects placed on it
@dataclass
class Square:
    ground: Object = None
    objects: List[Object] = field(default_factory=list)

    def append(self, object: Object) -> NoReturn:
        # We might rename the walkable property into sth like ground
        if object.walkable and self.ground != None:
            # In the future when we add logger we should log this event!
            raise Exception("Cannot put more than a one ground in a square!")
        
        if object.walkable:
            self.ground = object

        self.objects.append(object)

    def remove(self, object: Object) -> NoReturn:
        if self.ground == object:
            self.ground = None
        
        self.objects.remove(object)