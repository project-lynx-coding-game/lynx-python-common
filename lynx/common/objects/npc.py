import random

from lynx.common.state_machine import StateMachine
from lynx.common.point import Point
from lynx.common.objects.object import Object
from lynx.common.serializable import Properties
from lynx.common.actions.move import Move
from lynx.common.actions.idle import Idle
from lynx.common.enums import Direction


class NPC(Object):
    """
    NPC interface.
    """
    base: str
    properties: Properties
    scene: 'Scene'
    walkable: bool
    machine: StateMachine
    hp: int

    def __init__(self, scene: 'Scene', position: Point, hp: int, machine: StateMachine) -> None:
        super().__init__(position, scene)
        self.machine = machine
        self.hp = hp

    def move(self):
        Move(self, random.choice(list(Direction))).execute()

    def idle(self):
        Idle(self).execute()
