from dataclasses import dataclass

from lynx.common.actions.action import Action


@dataclass
class MessageLog(Action):
    """
    Simple action for logging debug information
    """
    object_id: int = -1
    text: str = ""

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return True

    def apply(self, scene: 'Scene') -> None:
        pass
