from lynx.common.actions.action import Action
from lynx.common.serializable import Properties


class WaitForCode(Action):
    """
    Action blocking execution of the runtime until it reads
    message from `stdin` saying that the `code` was uploaded
    """
    base: str
    interactive: bool
    properties: Properties

    def __init__(self, interactive: bool) -> None:
        super().__init__()
        self.interactive = interactive

    def execute(self) -> None:
        if not self.interactive:
            return

        self.log()
        message: str = input()
        if message != "CODE UPLOADED":
            exit(1)
