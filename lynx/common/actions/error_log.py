from dataclasses import dataclass

from lynx.common.actions.action import Action


@dataclass
class ErrorLog(Action):
    """
    Simple action for logging errors during runtime
    """
    text: str = ""
    user_id: str = ""

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return True

    def apply(self, scene: 'Scene') -> None:
        pass
