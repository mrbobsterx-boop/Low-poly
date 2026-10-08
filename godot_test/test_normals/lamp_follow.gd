extends PointLight2D
# Лампа ходит за мышкой — обведите её вокруг многогранника.


func _process(_delta: float) -> void:
	global_position = get_global_mouse_position()
