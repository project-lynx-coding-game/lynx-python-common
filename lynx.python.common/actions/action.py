from lynx.python.common.serializable import Serializable, Properties


class Action(Serializable):
    """
    Represents abstract object responsible for interacting
    with a `scene`.
    """
    base: str
    properties: Properties

    def __init__(self) -> None:
        super().__init__(__class__.__name__)

    def execute(self) -> None:
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
