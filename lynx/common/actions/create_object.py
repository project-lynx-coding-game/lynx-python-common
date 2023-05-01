from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.object import Object


@dataclass
class CreateObject(Action):
	"""
	ACtion for adding new objects to the world map.
	"""
	object_str: str = ""

	def apply(self, scene: 'Scene') -> None:
		object = Object.deserialize(self.object_str)
		scene.add_entity(object)

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		object = Object.deserialize(self.object_str)
		# There mustn't be an object with such id already
		return scene.get_object_by_id(object.id) is None
