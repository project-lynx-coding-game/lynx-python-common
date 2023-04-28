from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.object import Object


@dataclass
class CreateObject(Action):
	"""
	Function for adding new objects to the world map.
	"""
	object_str: str = ""

	def apply(self, scene: 'Scene') -> None:
		object = Object.deserialize(self.object_str)
		scene.add_entity(object)

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		return True
