from typing import Callable, List

from lynx.common.enitity import Entity


class Action(Entity):
    """
    Represents abstract object responsible for interacting
    with a `scene`.
    """

    # TODO: maybe we should change the interface to be a part of 
    # `Scene`, so scene will call scene.apply(action)
    def apply(self, scene: 'Scene') -> None:
        """
        Method used to change state of a `scene`
        """

    def satisfies_requirements(self, scene: 'Scene') -> bool:
        """
        Method returns all requirements needed to apply changes
        """
