from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.object import Object


@dataclass
class Hide(Action):
	"""
	We need this to make objects disappear from map, but withour removing them forever.
	"""
	object_id: int = -1

	def apply(self, scene: 'Scene') -> None:
		object: Object = scene.get_object_by_id(self.object_id)
		object.hidden = True
		scene.remove_from_map(object)

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		return True			##add object is not none etc.
