from dataclasses import dataclass
from lynx.common.vector import Vector
from lynx.common.actions.action import Action
from lynx.common.object import Object

@dataclass
class Move(Action):
    """
    Simple action for changing position of `Object`. It does not log anything
    in case the movement was not possible(destination is not walkable etc).
    """
    object_id: int = -1
    vector: Vector = Vector(0,0)

    def execute(self, scene) -> None:
        # TODO: Right now, actions are not doing anything on the Python side
        #       real changes are made by `scene-host`
        pass
