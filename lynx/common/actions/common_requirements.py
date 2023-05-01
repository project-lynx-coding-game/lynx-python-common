from lynx.common.object import Object
from lynx.common.square import Square
from lynx.common.vector import Vector


class CommonRequirements:

	@staticmethod
	def is_walkable(scene: 'Scene', object_id: int, movement: Vector) -> bool:
		object: Object = scene.get_object_by_id(object_id)
		destination_position: Vector = object.position + movement
		square_at_destination: Square = scene.get_square(destination_position)
		return square_at_destination.walkable()

	@staticmethod
	def is_on_square(scene: 'Scene', position: Vector, name: str) -> bool:
		objects_on_square = scene.get_objects_by_position(position)
		return name in [object.name for object in objects_on_square]

	@staticmethod
	def is_in_range(scene: 'Scene', object_id: int, position: Vector, max_distance: int) -> bool:
		object: Object = scene.get_object_by_id(object_id)
		distance = object.position.dist_to(position)
		return distance <= max_distance
