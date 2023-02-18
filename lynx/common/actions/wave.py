from lynx.common.actions.action import Action
from lynx.common.serializable import Properties


class Wave(Action):
    """
    Simple action for playing an animation on frontend.
    """
    base: str
    properties: Properties

    def __init__(self, agent: 'Agent') -> None:
        super().__init__()
        self.properties.agent_id = agent.properties.id

    def execute(self) -> None:
        self.log()
