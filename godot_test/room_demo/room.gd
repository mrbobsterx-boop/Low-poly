extends Node2D
# Комната, как в игре: оболочка (сегмент, края, перекрытия) + предметы по layout.json. Картинки — чистые,
# свет — Godot по картам нормалей. Масштаб: рендер 200 px/м → здесь 0.5 → 100 px/м (как в игре), камера ×2.
const PX := 100.0
var floor_y := 0.0
var left_x := 0.0

func spr(name: String, pos: Vector2, centered_bottom := false) -> Sprite2D:
	var ct := CanvasTexture.new()
	ct.diffuse_texture = load("res://room_demo/art/%s.png" % name)
	ct.normal_texture = load("res://room_demo/art/%s_n.png" % name)
	var s := Sprite2D.new()
	s.texture = ct
	s.centered = false
	s.scale = Vector2(0.5, 0.5)
	var sz: Vector2 = ct.diffuse_texture.get_size() * 0.5
	s.position = pos - (Vector2(sz.x / 2, sz.y) if centered_bottom else Vector2(0, sz.y))
	add_child(s)
	return s

func light(pos: Vector2, color: Color, energy: float, scale_: float, h: float) -> void:
	var grad := Gradient.new()
	grad.colors = PackedColorArray([Color(1, 1, 1, 1), Color(1, 1, 1, 0)])
	var tex := GradientTexture2D.new()
	tex.gradient = grad
	tex.width = 256
	tex.height = 256
	tex.fill = GradientTexture2D.FILL_RADIAL
	tex.fill_from = Vector2(0.5, 0.5)
	tex.fill_to = Vector2(0.5, 0.0)
	var l := PointLight2D.new()
	l.texture = tex
	l.texture_scale = scale_
	l.color = color
	l.energy = energy
	l.height = h
	l.position = pos
	add_child(l)

func _ready() -> void:
	var lay: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://room_demo/layout.json"))
	var w: float = lay["width_m"] * PX
	left_x = 50.0
	floor_y = 420.0
	var cm := CanvasModulate.new()
	cm.color = Color(0.20, 0.21, 0.27)
	add_child(cm)
	var shell: String = lay["shell"]
	spr(shell + "_mid", Vector2(left_x, floor_y))
	spr(shell + "_left", Vector2(left_x - 50, floor_y))
	spr(shell + "_right", Vector2(left_x + w, floor_y))
	for it in lay["items"]:
		var x: float = left_x + float(it["x_m"]) * PX
		var y: float = floor_y - float(it["bottom_m"]) * PX
		spr(it["image"], Vector2(x, y), true)
	for y in [floor_y - 4 * PX, floor_y]:
		var x := left_x - 50 - 300
		while x < left_x + w + 50:
			spr("slab_bunker_concrete_normal", Vector2(x, y + PX))
			x += 512
	light(Vector2(left_x + 256, floor_y - 290), Color(1.0, 0.72, 0.42), 2.2, 3.4, 140.0)
	light(Vector2(left_x + 110, floor_y - 200), Color(1.0, 0.70, 0.40), 0.9, 2.0, 120.0)
	light(Vector2(left_x + 400, floor_y - 200), Color(1.0, 0.70, 0.40), 1.0, 2.2, 120.0)
	var cam := Camera2D.new()
	cam.zoom = Vector2(2, 2)
	cam.position = Vector2(left_x + w / 2, floor_y - 180)
	add_child(cam)
	cam.make_current()
