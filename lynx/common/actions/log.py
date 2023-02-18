from lynx.common.actions.action import Action
from lynx.common.serializable import Properties


class Log(Action):
    """
    Action sending message as runtimes log
    """
    base: str
    interactive: bool
    properties: Properties

    def __init__(self, type: str, message: str) -> None:
        super().__init__()
        self.properties.type = type
        self.properties.message = message

    def execute(self) -> None:
        self.log()
