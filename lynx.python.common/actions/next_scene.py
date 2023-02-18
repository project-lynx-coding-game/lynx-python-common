from lynx.python.common.scene import Scene
from lynx.python.common.actions.action import Action
from lynx.python.common.serializable import Properties


class NextScene(Action):
    """
    `Action` used to create next scene. Called on collision by `Portal`.
    """
    base: str
    properties: Properties
    runtime: 'Runtime'

    def __init__(self, runtime: 'Runtime') -> None:
        super().__init__()
        self.runtime = runtime

    def execute(self) -> None:
        """
        The execution of this `Action` is quite problematic, because
        it uses EXISTING instance of scene and calls its constructor
        once again. Subject to further refactoring.
        """
        self.log()
        self.runtime.scene = Scene(self.runtime)
        self.runtime.scenes.append(self.runtime.scene)
