# Проба стиля: одна комната в трёх стилях

Цель — выбрать стиль **до** того, как делать все 180 объектов. Одна и та же комната убежища (жилая) делается
три раза: **A — Low poly**, **B — Реализм** (как сейчас), **C — Рисованный** (как Fallout Shelter). Игра покажет
комнату во всех трёх стилях, переключение — **Tab**. Автор смотрит и выбирает.

**Куда класть:** Google Диск → «Shelter Tripo» → «00 Проба стиля (одна комната)» → папка стиля
(A — Low poly / B — Реализм / C — Рисованный). **Имена файлов — как в таблице** (одинаковые во всех трёх папках,
стиль определяет папка): `bed.glb`, `locker.glb`…

---

## Как составить запрос

Запрос = **начало стиля** (раздел 1, одно на все предметы этого стиля) + **строка предмета** (раздел 2) + **конец**:

```
Single object, front view, isolated, nothing around it, no floor, no background, no text, no letters.
```

Пример для кровати в стиле A: начало A + строка кровати + конец — всё одним абзацем.

---

## 1. Три стиля

### A — Low poly
Простые грани, мало деталей, ровные цвета — как в инди-играх (Unturned, Superhot, Firewatch-упрощённо).
Лёгкие модели, хорошо смотрятся издалека, на Steam Deck быстрее всего.
```
Low poly stylized 3D game asset, simple geometric shapes with flat-shaded faces, very few polygons,
clean solid colors, muted post-apocalyptic palette of rust orange, olive green, concrete grey and dark brown,
no small details.
```
Tripo: если есть режим **Low Poly / Smart Low Poly** — включить; полигоны **3 000–5 000**; текстура — вкл, **1K**;
«Удалить освещение» — вкл; PBR — выкл (если можно).

### B — Реализм (как сейчас)
Как верстаки, которые уже в игре: фото-текстуры, ржавчина, грязь.
```
Realistic 3D game asset, worn and weathered, from an old underground fallout bunker, realistic PBR texture
with rust, dirt, chipped paint and scratches.
```
Tripo: HD; полигоны **50 000–100 000** (мелочь — 20 000); текстура — вкл, **2K**; «Удалить освещение» — вкл; PBR — вкл.

### C — Рисованный (как Fallout Shelter)
Чуть «мультяшные», крепкие формы, мягкие нарисованные текстуры, ретро 1950-х. Читается с любого расстояния.
```
Stylized 3D game asset in a hand-painted style similar to Fallout Shelter, chunky slightly exaggerated proportions,
soft hand-painted textures, clear readable shapes, retro 1950s underground vault look, a bit worn and dirty.
```
Tripo: если есть стиль **Cartoon / Stylized** — включить; полигоны **20 000–30 000**; текстура — вкл, **2K**;
«Удалить освещение» — вкл.

---

## 2. Что в комнате (одинаково для всех стилей)

Комната: ширина 6 м, высота 3 м, глубина 3 м, спереди открыта (разрез, как в игре). Размер — **ширина × высота ×
глубина**, в запросе его писать не нужно (Tripo держит пропорции из описания, точный размер выставит обработка).

### Оболочка комнаты

| № | Файл | Что | Размер, м | Строка предмета |
|---|---|---|---|---|
| 1 | `floor.glb` | пол, кусок | 3 × 0,1 × 3 | `A square floor tile section of a bunker room, old concrete floor with cracks and stains, flat slab, seen from above at an angle.` |
| 2 | `wall_back.glb` | задняя стена, пустая | 3 × 3 × 0,3 | `A plain flat wall segment, square, concrete panels with seams, perfectly straight edges on all sides, no border, no frame, nothing on the wall.` |
| 3 | `wall_side_door.glb` | боковая стена с дверным проёмом | 3 × 3 × 0,3 | `A flat side wall segment of a bunker room, concrete, with a rectangular doorway opening 1.1 m wide near one edge, straight edges, nothing on the wall.` |
| 4 | `wall_side.glb` | боковая стена без проёма | 3 × 3 × 0,3 | то же, что №2, но `side wall of a bunker room` |
| 5 | `ceiling.glb` | потолок, кусок | 3 × 0,15 × 3 | `A flat ceiling slab section of a bunker room, concrete with a few rivets and stains, seen from below at an angle.` |

### Линии (через всю стену)

| № | Файл | Что | Размер, м | Строка предмета |
|---|---|---|---|---|
| 6 | `line_pipes.glb` | две трубы | 3 × 0,25 × 0,2 | `A straight horizontal section of two parallel industrial pipes on small metal brackets, both ends cut perfectly flat, no caps, flat back side.` |
| 7 | `line_cable.glb` | кабели | 3 × 0,08 × 0,06 | `A straight horizontal bundle of three electric cables held by metal clips, both ends cut flat, flat back side.` |

### Декор на стенах

| № | Файл | Что | Размер, м | Строка предмета |
|---|---|---|---|---|
| 8 | `decor_vent.glb` | решётка вентиляции | 0,5 × 0,5 × 0,05 | `A square metal ventilation grille mounted on a wall, flat back side.` |
| 9 | `decor_box.glb` | щиток с проводами | 0,35 × 0,5 × 0,12 | `A small electrical junction box mounted on a wall with a short bundle of wires going up, flat back side.` |
| 10 | `poster_1.glb` | плакат (люди и солнце) | 0,6 × 0,8 × 0,02 | `A slightly torn retro poster on a wall showing a smiling family and a big sun, pictures only, flat.` |
| 11 | `poster_2.glb` | плакат (схема убежища) | 0,8 × 0,6 × 0,02 | `An old paper poster with a simple drawing of an underground shelter cross-section, pictures only, curled corners, flat.` |
| 12 | `wall_shelf.glb` | полка на стене с банками | 1 × 0,35 × 0,3 | `A small wall shelf made of wood and metal brackets with a few cans and jars on it, flat back side.` |

### Мебель и вещи

| № | Файл | Что | Размер, м | Строка предмета |
|---|---|---|---|---|
| 13 | `bed.glb` | кровать (железная койка) | 2 × 0,8 × 0,9 | `A single metal frame bed with a thin mattress, a pillow and a folded wool blanket.` |
| 14 | `workbench.glb` | верстак | 1,6 × 0,95 × 0,8 | `A sturdy wooden workbench with a vise and a few tools hanging on a small back board.` |
| 15 | `locker.glb` | шкафчик | 0,6 × 1,8 × 0,5 | `A tall narrow metal locker with two vent slots and a handle, slightly dented.` |
| 16 | `stove.glb` | печка-буржуйка (камин) | 0,6 × 1 × 0,6 | `A small cast iron wood-burning stove with a chimney pipe going up, a little door with glowing coals.` |
| 17 | `table.glb` | стол | 1,2 × 0,75 × 0,7 | `A simple old wooden table with four legs.` |
| 18 | `chair.glb` | стул | 0,45 × 0,9 × 0,45 | `A simple old wooden chair.` |
| 19 | `lamp_ceiling.glb` | лампа под потолком | 0,35 × 0,4 × 0,35 | `A hanging industrial ceiling lamp with a metal shade and a wire cage around the bulb.` |
| 20 | `crate.glb` | ящик | 0,8 × 0,5 × 0,5 | `A wooden supply crate with metal corners and stencil marks without letters.` |
| 21 | `barrel.glb` | бочка с водой | 0,6 × 0,9 × 0,6 | `A metal water barrel with a tap near the bottom.` |
| 22 | `radio.glb` | радиоприёмник (на стол) | 0,4 × 0,3 × 0,25 | `An old tube radio receiver with knobs and a dial.` |

### Персонаж

| № | Файл | Что | Размер, м | Строка предмета |
|---|---|---|---|---|
| 23 | `character.glb` | выживший | 0,5 × 1,8 × 0,3 | `A full body survivor character standing in a T-pose, adult man in a worn jumpsuit with a utility belt and boots, short hair.` |

Персонаж — только посмотреть стиль (стоит неподвижно). Анимации — потом, после выбора стиля (у Tripo есть авто-риг).

**Итого: 23 модели × 3 стиля.** Можно начать с половины в каждом стиле (2, 6, 8, 10, 13, 14, 15, 16, 19, 23) —
этого хватит, чтобы сравнить.

---

## 3. Обработка (второй чат)

- Скачать с Диска: папка «00 Проба стиля», три подпапки (ссылки на файлы — в `tripo/style_test.json`, заполняет чат игры).
- Каждую модель: перед — к −Y, низ — в Z = 0, **размер — из таблицы раздела 2** (не из ОС). Висящее на стене —
  спина в Y = 0; лампа — верх в Z = 0.
- Облегчить: A — как есть (≤ 5 000), B и C — мебель ≤ 8 000, стены и пол ≤ 4 000, мелочь ≤ 3 000, персонаж ≤ 15 000.
  Текстуры 1024. Без блеска.
- Экспорт: `export/style_test/<a|b|c>/<имя>_idle.glb`. Лист превью — три ряда (A, B, C), все модели.

## 4. Игра (чат игры)

Комната «Проба стиля» (в главном меню или в редакторе сцены): пол, стены, линии, декор, мебель и персонаж стоят
одинаково, **Tab** — переключить стиль A → B → C; подпись, какой стиль сейчас. Автор смотрит и выбирает.
После выбора — общий план всех объектов в выбранном стиле (`docs/TRIPO_OBJECTS.md`).
