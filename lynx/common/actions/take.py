from dataclasses import dataclass
from lynx.common.actions.action import Action
from lynx.common.actions.hide import Hide
from lynx.common.object import Object
from lynx.common.actions.common_requirements import CommonRequirements


@dataclass
class Take(Action):
	"""
	Action to pick up object from square on which we stand. Imo we should give string of objetct's name, so we won't
	pick every `pickable` object from square.
	"""
	object_id: int = -1
	object_to_pick: str = ""

	def apply(self, scene: 'Scene') -> None:
		object: Object = scene.get_object_by_id(self.object_id)
		objects_on_square = scene.get_objects_by_position(object.position)
		for square_object in objects_on_square:
			if square_object.name == self.object_to_pick and square_object.pickable is True:
				object.inventory.append(square_object.id)
				hide_action = Hide(square_object.id)
				scene.add_to_pending_actions(hide_action.serialize())
				break

	def satisfies_requirements(self, scene: 'Scene') -> bool:
		object: Object = scene.get_object_by_id(self.object_id)
		return CommonRequirements.does_pickable_object_exists_on_square(scene, object.position, self.object_to_pick)
