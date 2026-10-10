# Стены и фасады из Tripo — каталог (что делать, по порядку)

Решение автора (2026-10-10): стены **не делаются целыми кусками с трубами**. Каждая стена — из трёх слоёв:

| Слой | Что это | Как ставит игра |
|---|---|---|
| **1. Основа** | Пустая стена: бетон, плитка, доски, обои, кирпич. Без труб и предметов, края ровные | Кусками в ряд по ширине комнаты (сколько влезет, каждый чуть растягивается) |
| **2. Линии** | То, что тянется через всю стену: трубы, кабель, плинтус, карниз | Одной ровной линией на всю ширину, на одной высоте |
| **3. Декор** | Мелочь на стене: решётка вентиляции, щиток, трещина, картина, окно | 0–3 штуки на стену, случайно, не друг на друге |

Так любые куски стыкуются, трубы не обрываются, а стены разных комнат выглядят по-разному.

**Что НЕ декор, а объект игры (из ОС):** полки, лампы, ящики, щиты-генераторы, шкафы — их можно двигать, ломать,
обыскивать. Декор — только «нарисованное» на стене, с ним ничего не делают.

---

## 1. Общие правила для всех моделей

- Tripo: **Text to Model**; HD; AI-дополнение — выкл; текстура — вкл, 2K; «Удалить освещение» — вкл; PBR — вкл.
  Полигоны: основа и фасад — 20 000; линии и декор — 10 000.
- **В запросе не писать цифры высот** («at 2.4 m») — Tripo рисует их прямо на стене.
- Основа: **без окантовки, рамки, бортика** по краям — края ровные со всех четырёх сторон.
- Цвет — **спокойный, нейтральный**: игра может подкрашивать стены по типу комнаты.
- Скачать GLB, назвать **точно как в таблице**, загрузить в
  [tripo/](https://github.com/mrbobsterx-boop/Low-poly/upload/main/tripo) (Add file → Upload files → Commit changes).
- `<N>` — номер варианта: 1, 2, 3. Вариантов основы — **2–3 на набор** (отличаются только пятнами и потёками).
- Сначала **одна** модель каждого вида — проверить в игре, потом остальные.

Общее начало запроса **основы** (дописать строку набора из раздела 2):
```
A single flat wall segment, front view, square, 3 m wide, 3 m tall, 30 cm thick. A flat slab with
perfectly straight flat edges on all four sides, no border, no frame, no trim, no edging.
Nothing on the wall: no pipes, no cables, no objects. Game asset, realistic texture.
```

Общее начало запроса **линии** (дописать строку из раздела 3):
```
A straight horizontal element, 3 meters long, front view, flat back side, both ends cut perfectly flat
(no caps, no flanges), no wall behind it. Game asset, realistic texture.
```

Общее начало запроса **декора** (дописать строку из раздела 4):
```
A single object mounted on a wall, front view, flat back side, no wall behind it, nothing around it.
Game asset, realistic texture.
```

---

## 2. Основы — наборы стен

### Убежище (бункер)

| Набор | Файл | Какие комнаты | Строка в конец запроса основы |
|---|---|---|---|
| Бетон | `room_concrete_wall_<N>.glb` | шлюз, склад, машинная, гараж | `Weathered grey concrete panels with seams, rust streaks, dirt and water stains.` |
| Крашеный бетон | `room_painted_wall_<N>.glb` | жилая | `Old concrete wall painted dark green on the lower half and dirty off-white on the upper half, peeling paint, scratches.` |
| Плитка | `room_tile_wall_<N>.glb` | кухня, насосная | `Old square ceramic tiles, pale green-grey, cracked and dirty grout, some tiles missing.` |
| Доски | `room_wood_wall_<N>.glb` | мастерская, оранжерея | `Rough vertical wooden planks nailed over concrete, old and darkened, some gaps.` |

### Дома (внутри)

| Набор | Файл | Какие комнаты | Строка в конец запроса основы |
|---|---|---|---|
| Обои | `room_wallpaper_wall_<N>.glb` | комната, спальня, офис | `Old faded wallpaper with a simple pattern, torn and peeling in places, stains.` |
| Белая плитка | `room_whitetile_wall_<N>.glb` | ванная, медпункт | `Old white square ceramic tiles, yellowed, cracked, dirty grout.` |
| Вагонка | `room_panel_wall_<N>.glb` | магазин | `Painted horizontal wooden wall panels, faded light brown paint, scratches.` |

---

## 3. Линии — через всю стену

| Файл | Где | Высота (ставит игра) | Строка в конец запроса линии |
|---|---|---|---|
| `room_line_pipes.glb` | бетон, крашеный, плитка, доски | под потолком | `Two parallel rusty industrial pipes on small metal brackets.` |
| `room_line_cable.glb` | бетон, крашеный | чуть ниже труб | `A bundle of three black electric cables held by metal clips.` |
| `room_line_baseboard.glb` | обои, белая плитка, вагонка | у пола | `A simple old wooden baseboard, 10 cm tall, scratched paint.` |
| `room_line_wire.glb` | обои, вагонка | под потолком | `An old twisted electric wire on small white ceramic insulators.` |

Одна модель линии — на все наборы, где она есть (трубы одинаковые во всём бункере).

---

## 4. Декор — на стене

### Убежище

| Файл | Что это | Строка в конец запроса декора |
|---|---|---|
| `room_decor_vent.glb` | решётка вентиляции | `A square rusty metal ventilation grille, 50 cm.` |
| `room_decor_box.glb` | щиток с проводами | `A small grey electrical junction box with a short bundle of wires going up.` |
| `room_decor_valve.glb` | труба с вентилем | `A vertical rusty pipe 2 m long with a red valve wheel in the middle.` |
| `room_decor_crack.glb` | пролом с арматурой | `A flat patch of broken concrete with exposed rusty rebar, 1 m wide.` |
| `room_decor_hatch.glb` | лючок в стене | `A small square metal service hatch with rivets, 60 cm.` |
| `room_decor_sign.glb` | табличка | `A small faded metal warning sign with a simple pictogram, no text.` |

### Дома

| Файл | Что это | Строка в конец запроса декора |
|---|---|---|
| `room_decor_window.glb` | окно изнутри | `A wooden house window seen from inside, 1.2 m wide, dirty glass, peeling paint.` |
| `room_decor_window_boarded.glb` | заколоченное окно | `A wooden house window seen from inside, boarded up with planks.` |
| `room_decor_picture.glb` | картина | `An old framed landscape painting, faded, slightly crooked.` |
| `room_decor_stain.glb` | пятно сырости | `A flat patch of damp mold stain on a wall, 1 m, very thin.` |
| `room_decor_clock.glb` | часы | `An old round wall clock, broken glass.` |

Какой декор в каком наборе — настройка игры (`data/config/view3d.json`, `wall_kit`), менять можно без моделей.

---

## 5. Фасады — дома снаружи

Фасад — то же самое: основа (кусок одного этажа 3 × 3 м) + линии (цоколь внизу, карниз наверху) + декор (окна, дверь).
Игра собирает фасад любой ширины и этажности.

| Набор | Файл основы | Строка в конец запроса основы |
|---|---|---|
| Кирпич | `facade_brick_wall_<N>.glb` | `Exterior wall of an old red brick house, weathered bricks, dirt.` |
| Штукатурка | `facade_plaster_wall_<N>.glb` | `Exterior wall of an old house, cracked beige plaster, patches of exposed brick.` |
| Доски | `facade_wood_wall_<N>.glb` | `Exterior wall of an old wooden house, horizontal grey weathered siding boards.` |
| Бетон (вход в бункер) | `facade_bunker_wall_<N>.glb` | `Exterior wall of a concrete bunker entrance, massive grey concrete, rust stains.` |

| Файл | Что это | Строка в конец запроса (начало — декора или линии) |
|---|---|---|
| `facade_line_roof.glb` | карниз (линия) | `An old roof edge cornice with a rusty gutter.` |
| `facade_line_base.glb` | цоколь (линия) | `A dark grey concrete plinth strip at the bottom of a house wall, 40 cm tall.` |
| `facade_decor_window.glb` | окно снаружи | `A house window seen from outside, 1.2 m wide, wooden frame, dirty dark glass.` |
| `facade_decor_window_broken.glb` | разбитое окно | `A house window seen from outside, broken glass, frame partly missing.` |
| `facade_decor_window_boarded.glb` | заколоченное | `A house window seen from outside, boarded up with planks.` |
| `facade_decor_door.glb` | дверь | `An old wooden house front door with a small canopy.` |

Окна игра ставит **рядами по этажам**, на одной высоте (не случайно). Свет в окне ночью — игра.

---

## 6. Порядок работы

1. **Проба:** `room_concrete_wall_1` + `room_line_pipes` + `room_decor_vent` + `room_decor_box`. → второй чат →
   игра. Смотрим одну комнату бункера. Нравится — дальше.
2. Остальные основы бункера (по 2 варианта) + `room_line_cable` + остальной декор убежища.
3. Дома внутри: обои, белая плитка, вагонка + плинтус + декор домов.
4. Фасады.

## 7. Как проверить модель до загрузки

- Основа — **плоская плита**, края ровные, без рамки; ничего не висит.
- Линия — **прямая**, концы обрезаны ровно, без заглушек; стены сзади нет.
- Декор — **один предмет**, спина плоская, стены вокруг нет.
- На модели **нет цифр и надписей**.

## 8. Кто что делает дальше

- **Второй чат (low-poly):** обработка по `docs/TRIPO.md` (раздел 5): основа — высота 3 м, пропорции свои, толщина
  0,3 м; линия — длина как есть, спина в плоскости стены; декор — размер как в запросе, спина в плоскости стены.
  Перед — к −Y. Экспорт `export/<имя>_idle.glb`.
- **Игра:** ставит основу кусками, линии на всю ширину, декор случайно (одинаково при каждом запуске).
  Настройки — `data/config/view3d.json` → `wall_kit`.
