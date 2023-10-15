from lynx.common.agent import Agent
from lynx.common.object import *
from lynx.common.serializable import Serializable
from lynx.common.vector import Vector


@dataclass
class Player(Serializable):
    player_id: str = field(default_factory=str)
    player_resources: Dict[str, int] = field(default_factory=dict)
    drop_area: Vector = field(default_factory=Vector)
    agents: dict[str, Agent] = field(default_factory=dict)

    def add_agent(self, agent: Agent) -> None:
        self.agents[agent.id] = agent

    def get_agents(self) -> list[Agent]:
        agents = list(self.agents.values())
        for agent in agents:
            agent.lifetime = agent.calculate_lifetime()

        return agents

    def get_agent_by_id(self, agent_id: int) -> Agent:
        agent = self.agents.get(agent_id)
        if not agent:
            return None

        agent.lifetime = agent.calculate_lifetime()
        return agent
