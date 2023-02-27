from lynx.common.enitity import Entity

class Action(Entity):
    """
    Represents abstract object responsible for interacting
    with a `scene`.
    """


    def execute(self, scene: 'Scene') -> None:
        """
        Method used to change state of a `scene` or `runtime`
        """

    def log(self) -> None:
        """
        Simple method logging `Action`, so frontend applications
        can modify visible state of the scene on their own.
        This method should not modify state of the scene.
        """
        print(self)
