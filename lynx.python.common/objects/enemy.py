from lynx.python.common.state_machine import StateMachine
from lynx.python.common.objects.npc import NPC
from lynx.python.common.point import Point
from lynx.python.common.serializable import Properties


class Enemy(NPC):
    """
    Enemy interface.
    """
    base: str
    properties: Properties
    scene: 'Scene'
    walkable: bool
    machine: StateMachine
    hp: int

    def __init__(self, scene: 'Scene', position: Point, hp: int, machine: StateMachine) -> None:
        super().__init__(scene, position, hp, machine)
