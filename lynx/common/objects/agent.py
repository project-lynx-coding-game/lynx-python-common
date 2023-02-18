from lynx.common.objects import Object

class Agent(Object):
    """
    Simple agent existing in a `scene`.
    """

    def __init__(self, scene: 'Scene', position: Point = Point(0, 0)) -> None:
        super().__init__(position, scene)


    def tick(self) -> None:
        """
        Called on an `Object`, so it can perform some actions
        """
