from dataclasses import dataclass

from lynx.common.actions.action import Action
from lynx.common.vector import Vector
from lynx.common.actions.removeObject import RemoveObject
from lynx.common.actions.createObject import CreateObject
from lynx.common.object import Object
from lynx.common.actions.common_requirements import CommonRequirements

@dataclass
class Chop(Action):
	"""
	Simple action used to hit/destroy object, which stands on the given destination.
	"""
	object_id: int = -1
	position: Vector = Vector(1, 0)

	def apply(self, scene: 'Scene') -> None:
		objects_on_square = scene.get_objects_by_position(self.position)
		for object in objects_on_square:
			if object.name == 'tree':
				remove_action = RemoveObject(object.id)
				log = Object(id=scene.generate_id(), name='log', position=object.position, pickable=True)
				create_action = CreateObject(log.serialize())
				scene.add_to_pending_actions(remove_action.serialize())
				scene.add_to_pending_actions(create_action.serialize())

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		return CommonRequirements.is_in_range(scene, self.object_id, self.position, 1) and CommonRequirements.does_object_exists_on_square(scene, self.position, 'tree')
