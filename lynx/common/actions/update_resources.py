from dataclasses import dataclass
from typing import Dict
from dataclasses import field

from lynx.common.actions.action import Action


@dataclass
class UpdateResources(Action):
    """
    Simple action for updating points on fronted.
    """
    user_name: str = ""
    points_updated: Dict[str, int] = field(default_factory=dict)

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        return True

    def apply(self, scene: 'Scene') -> None:
        pass
