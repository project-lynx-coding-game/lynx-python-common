from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.actions.remove_object import RemoveObject
from lynx.common.actions.create_object import CreateObject
from lynx.common.object import Object
from lynx.common.actions.common_requirements import CommonRequirements

@dataclass
class Chop(Action):
	"""
	Simple action used to hit/destroy object, which stands on the given destination.
	"""
	object_id: int = -1
	target_position: Vector = Vector(1, 0)

	def apply(self, scene: 'Scene') -> None:
		objects_on_square = scene.get_objects_by_position(self.target_position)
		for object in objects_on_square:
			if object.name == 'Tree':
				remove_action = RemoveObject(object.id)
				log = Object(id=scene.generate_id(), name='Log', position=object.position, pickable=True)
				create_action = CreateObject(log.serialize())
				scene.add_to_pending_actions(remove_action.serialize())
				scene.add_to_pending_actions(create_action.serialize())

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		return CommonRequirements.is_in_range(scene, self.object_id, self.target_position, 1) and CommonRequirements.is_on_square(scene, self.target_position, 'Tree')
