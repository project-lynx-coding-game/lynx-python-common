from lynx.common.object import Object
from lynx.common.square import Square
from lynx.common.vector import Vector


class CommonRequirements:

	@staticmethod
	def is_walkable(scene: 'Scene', position: Vector) -> bool:
		square_at_destination: Square = scene.get_square(position)
		return square_at_destination.walkable()

	@staticmethod
	def is_on_square(scene: 'Scene', position: Vector, name: str) -> bool:
		objects_on_square = scene.get_objects_by_position(position)
		return name in [object.name for object in objects_on_square]

	@staticmethod
	def is_in_range(scene: 'Scene', object_id: int, position: Vector, max_distance: int) -> bool:
		object: Object = scene.get_object_by_id(object_id)

		if object is None:
			return False

		distance = object.position.dist_to(position)
		return distance <= max_distance

	# object can be stacked on a given position if an object with the same name is already there
	@staticmethod
	def can_be_stacked(scene: 'Scene', position: Vector, object_name: str) -> bool:
		objects_on_square = scene.get_objects_by_position(position)

		for object in objects_on_square:
			if object.name == object_name:
				return True

		return False
