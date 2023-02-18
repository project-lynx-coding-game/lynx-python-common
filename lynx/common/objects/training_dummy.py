from lynx.common.state_machine import StateMachine
from lynx.common.objects.npcs.enemy import Enemy
from lynx.common.point import Point
from lynx.common.serializable import Properties

TRAINING_DUMMY_HP = 100


class TrainingDummy(Enemy):
    """
    Enemy that does not do anything.
    """
    base: str
    properties: Properties
    scene: 'Scene'
    walkable: bool

    def __init__(self, scene: 'Scene', position: Point) -> None:
        super().__init__(scene, position, TRAINING_DUMMY_HP, TrainingDummyStateMachine(self))

    def tick(self) -> None:
        self.machine.tick()


class TrainingDummyStateMachine(StateMachine):
    def __init__(self, dummy: TrainingDummy):
        super().__init__()
        self.dummy = dummy
        self.add_state("idle")\
            .set_state("idle")

    def _state_logic(self):
        self.dummy.idle()

    def _enter_state(self, new_state, old_state):
        pass

    def _exit_state(self, old_state, new_state):
        pass
