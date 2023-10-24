from datetime import datetime

from lynx.common.actions.update_resources import UpdateResources
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
    max_agents: int = 1

    BASE_COSTS = {
        "Wood": 6,
        "Stone": 6,
    }

    @property
    def price_multiplier(self) -> int:
        return 2 ** (self.max_agents - 1)

    def alive_agents_count(self) -> int:
        return sum([1 for agent in self.agents.values() if agent.is_alive])

    def has_available_slot(self) -> bool:
        return self.alive_agents_count() < self.max_agents

    def can_purchase_slot(self) -> bool:
        for resource, base_cost in self.BASE_COSTS.items():
            current_cost = base_cost * self.price_multiplier
            if self.player_resources.get(resource, 0) < current_cost:
                return False

        return True

    def calculate_slot_cost(self) -> Dict[str, int]:
        cost = {}
        for resource, base_cost in self.BASE_COSTS.items():
            current_cost = base_cost * self.price_multiplier
            cost[resource] = current_cost

        return cost

    def purchase_slot(self, scene: 'Scene') -> None:
        resources_to_deduct = {}
        for resource, base_cost in self.BASE_COSTS.items():
            current_cost = base_cost * self.price_multiplier
            resources_to_deduct[resource] = -current_cost
            self.player_resources[resource] -= current_cost

        self.max_agents += 1
        update_resources_action = UpdateResources(self.player_id, resources_to_deduct)
        scene.add_to_pending_actions(update_resources_action.serialize())

    def create_and_add_agent_from_object(self, object: Object) -> Agent:
        agent = Agent(
            id=object.id,
            type=object.get_type(),
            time_creation=datetime.now().isoformat(),
            time_death=None,
            is_alive=True,
            tick=object.tick,
        )
        self.agents[agent.id] = agent

    def add_agent_from_object(self, object: Object) -> bool:
        if self.has_available_slot():
            self.create_and_add_agent_from_object(object)
            return True

        return False

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
