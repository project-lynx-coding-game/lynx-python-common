from dataclasses import dataclass

from lynx.common.actions.action import Action


@dataclass
class Print(Action):
    """
    Simple action for printing player's message
    """
    text: str = ""
    user_id: str = ""
    object_id: int = -1

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return True

    def apply(self, scene: 'Scene') -> None:
        pass
