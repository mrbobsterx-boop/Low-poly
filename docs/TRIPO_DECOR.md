# Декор, стены, пол и фоны — стиль «кровать-образец»

Решение автора (2026-10-10): цель — картинка-образец (разрез убежища: серо-синяя сталь, цветные комнаты, трубы,
лампочки, доски на полу, таблички, мелочи). Всё **мягко и чисто**, не «ржаво». Объекты (кровати, ящики…) — в
`TRIPO_OBJECTS.md`; здесь — то, что делает пустую комнату **живой**.

## Как делать (Tripo)

Как объекты: картинка-образец (кровать) → ✏️ → запрос из серого блока → картинка → «Создать» (HD) → **GLB**, имя —
как в списке, папка на Диске — в заголовке раздела. Пачка готова → «забери декор».

- **Стены (раздел 1)** — светло-серые: цвет комнаты игра ставит сама (`view3d.json` → `room_colors`).
- **Линии (раздел 2)** — прямые куски, концы ровные: игра стыкует их на всю ширину.
- **Таблички** — без букв (Tripo пишет криво).
- **Фоны (раздел 8)** — это **картинки, не 3D**: делаются генератором картинок, «Создать» не нажимать.

**Порядок (проба):** `room_steel_wall_1`, `room_line_pipes`, `room_line_bulbs`, `room_decor_pipes_vertical`,
`room_decor_tube_lamp`, `floor_planks` → чат игры ставит в одну комнату → смотрим → остальное.

---

## 1. Стены — основы (панель 3 × 3 м)

Папка на Диске: **01 Стены — основы**

Основа — пустая стена, игра ставит её кусками в ряд и **сама красит** в цвет комнаты (как на картинке-образце: синяя, жёлтая, красная, оливковая…). Поэтому основы — **светло-серые**. Делать по 2 варианта (`_1`, `_2`): запрос тот же, нажать «ещё раз».

**1. Стальные панели (убежище)** — `room_steel_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat bunker wall section made of large riveted steel panels with two vertical steel posts at the sides and a horizontal steel rail across the middle. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**2. Гофра (как контейнер)** — `room_container_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat wall section of corrugated metal sheet with vertical ribs, like the wall of a shipping container. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**3. Бетон** — `room_concrete_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat wall section of smooth concrete panels with visible seams and a few small bolt holes. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**4. Доски** — `room_wood_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat wall section of vertical wooden planks with small gaps between them. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**5. Плитка** — `room_tile_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat wall section covered with square ceramic tiles, the lower half tiled and the upper half plain painted plaster. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**6. Обои (дом)** — `room_wallpaper_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat house wall section with simple patterned wallpaper and a wooden baseboard at the bottom. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

**7. Кирпич** — `room_brick_wall_1.glb` · 300 × 300 см
```
Replace the bed with a flat wall section of painted brick. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, filling the picture. Light neutral grey color (the game will tint it), soft and clean, slightly worn, no rust. Perfectly straight flat edges on all four sides, no frame, no border, nothing attached. No text.
```

## 2. Линии — через всю стену

Папка на Диске: **02 Стены — линии**

Тянутся одной полосой на всю ширину комнаты. Делать **прямой кусок ~3 м**, концы ровные — игра стыкует куски.

**8. Трубы цветные (горизонтально)** — `room_line_pipes.glb` · 300 × 30 см
```
Replace the bed with a straight horizontal bundle of three parallel pipes, yellow, blue and red, on small grey metal brackets, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**9. Гирлянда лампочек** — `room_line_bulbs.glb` · 300 × 40 см
```
Replace the bed with a straight horizontal black cable hanging in gentle loops with five small glowing warm light bulbs hanging from it, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**10. Кабели в лотке** — `room_line_cable.glb` · 300 × 15 см
```
Replace the bed with a straight horizontal metal cable tray with a few black and grey cables inside, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**11. Балка под потолком** — `room_line_beam.glb` · 300 × 25 см
```
Replace the bed with a straight horizontal steel I-beam with rivets, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**12. Вентиляционный короб** — `room_line_duct.glb` · 300 × 40 см
```
Replace the bed with a straight horizontal square ventilation duct made of galvanized metal with seams, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**13. Плинтус** — `room_line_baseboard.glb` · 300 × 10 см
```
Replace the bed with a straight simple painted wooden baseboard strip, both ends cut flat. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

## 3. Вертикальное — у стены

Папка на Диске: **03 Стены — декор**

Стоят у стены от пола до потолка (3 м): разбивают пустую стену на части, как на образце.

**14. Трубы цветные (вертикально)** — `room_decor_pipes_vertical.glb` · 40 × 300 см
```
Replace the bed with a vertical bundle of three pipes, yellow, blue and red, going from floor to ceiling, held by one grey metal clamp plate in the middle. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**15. Стойка-колонна** — `room_decor_post.glb` · 30 × 300 см
```
Replace the bed with a vertical square steel support column with bolts at the top and bottom. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**16. Трубы с вентилями** — `room_decor_valves.glb` · 120 × 200 см
```
Replace the bed with three vertical grey pipes side by side, each with a red round valve wheel, joined by a horizontal pipe at the top. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**17. Кабель-канал** — `room_decor_conduit.glb` · 15 × 300 см
```
Replace the bed with a thin vertical grey conduit tube with a small junction box. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

## 4. Декор на стене

Папка на Диске: **03 Стены — декор**

Мелочь на стене: игра вешает 0–3 штуки на стену, случайно. Таблички — **с простым значком, без надписей** (Tripo портит буквы; надписи потом сделает игра).

**18. Лампа дневного света** — `room_decor_tube_lamp.glb` · 80 × 15 см
```
Replace the bed with a ceiling fluorescent tube lamp in a simple metal housing, glowing cold white. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**19. Красная аварийная лампа** — `room_decor_red_lamp.glb` · 20 × 25 см
```
Replace the bed with a small red emergency wall lamp in a metal cage, glowing red. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**20. Настенный фонарь** — `room_decor_wall_lamp.glb` · 25 × 40 см
```
Replace the bed with a small industrial wall lamp with a metal shade and a warm glowing bulb. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**21. Электрощиток** — `room_decor_fusebox.glb` · 50 × 60 см
```
Replace the bed with a grey metal electrical cabinet with a closed door, a lightning pictogram sticker and cables going up. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**22. Распределительная коробка** — `room_decor_box.glb` · 25 × 25 см
```
Replace the bed with a small grey junction box with two short cables. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**23. Решётка вентиляции** — `room_decor_vent.glb` · 50 × 50 см
```
Replace the bed with a square metal ventilation grille with slats. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**24. Табличка «опасно»** — `room_decor_sign_warning.glb` · 60 × 40 см
```
Replace the bed with a yellow and black warning sign plate with a simple exclamation pictogram, no letters. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**25. Табличка красная** — `room_decor_sign_red.glb` · 70 × 40 см
```
Replace the bed with a white sign plate with a red top band and simple pictogram, no letters. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**26. Доска объявлений** — `room_decor_noticeboard.glb` · 80 × 60 см
```
Replace the bed with a cork notice board with pinned paper notes and drawings, no readable text. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**27. Листки на стене** — `room_decor_papers.glb` · 60 × 50 см
```
Replace the bed with a cluster of yellowed paper notes and small drawings taped to a wall, no readable text, no wall behind. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**28. Плакат** — `room_decor_poster.glb` · 50 × 70 см
```
Replace the bed with a slightly faded poster with a simple cheerful illustration of a sun over mountains, taped at the corners, no text. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**29. Грифельная доска** — `room_decor_chalkboard.glb` · 60 × 80 см
```
Replace the bed with a small chalkboard with a wooden frame and a simple chalk smiley drawing, no text. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**30. Огнетушитель** — `room_decor_extinguisher.glb` · 20 × 55 см
```
Replace the bed with a red fire extinguisher on a small wall bracket. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**31. Часы** — `room_decor_clock.glb` · 30 × 30 см
```
Replace the bed with a round wall clock with a white face and simple black hands. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**32. Полосы опасности** — `room_decor_hazard.glb` · 100 × 15 см
```
Replace the bed with a flat strip of yellow and black diagonal hazard stripes painted on a metal plate. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**33. Карта** — `room_decor_map.glb` · 80 × 60 см
```
Replace the bed with a pinned paper map of a region with a few red marks and strings, no readable text. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**34. Шланг на крючке** — `room_decor_hose.glb` · 40 × 50 см
```
Replace the bed with a coiled garden hose hanging on a metal hook. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**35. Инструменты на щите** — `room_decor_tools.glb` · 80 × 60 см
```
Replace the bed with a perforated pegboard with a hammer, wrench, saw and pliers hanging on it. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

## 5. Пол

Папка на Диске: **03 Стены — декор**

Лежат на полу — делают пол живым (доски, ковры). Высота почти ноль; показывать **немного сверху**.

**36. Деревянный настил** — `floor_planks.glb` · 150 × 5 см
```
Replace the bed with a flat rectangular wooden floor pallet made of light planks laid side by side, very low, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**37. Ковёр** — `floor_rug.glb` · 200 × 2 см
```
Replace the bed with a flat worn rectangular rug with a simple red and beige pattern, lying flat, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**38. Коврик у кровати** — `floor_rug_small.glb` · 80 × 2 см
```
Replace the bed with a small flat round braided rug, lying flat, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**39. Резиновый мат** — `floor_mat.glb` · 120 × 3 см
```
Replace the bed with a flat black ribbed rubber floor mat, lying flat, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**40. Решётка в полу** — `floor_grate.glb` · 100 × 3 см
```
Replace the bed with a flat square metal floor grate, lying flat, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**41. Люк в полу** — `floor_hatch.glb` · 80 × 5 см
```
Replace the bed with a flat round metal floor hatch with a handle, lying flat, seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

## 6. Двери и проёмы

Папка на Диске: **09 Строительное и двери**

**42. Гермодверь с колесом** — `door_vault.glb` · 120 × 220 см
```
Replace the bed with a heavy round-cornered bunker vault door painted red with a big round valve wheel in the middle and rivets around. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**43. Стальная двустворчатая** — `door_double_steel.glb` · 180 × 230 см
```
Replace the bed with a double steel door, one leaf open, grey with yellow and black hazard stripes at the top. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**44. Арка-тоннель** — `room_arch.glb` · 300 × 300 см
```
Replace the bed with the round end of a bunker tunnel: a half-circle arch made of curved steel ribs and wooden planks, open towards the viewer. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**45. Дверной проём с рамой** — `door_frame.glb` · 120 × 230 см
```
Replace the bed with an empty steel door frame with a small lamp above it. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

## 7. Мелочи для жизни (на пол, у стены)

Папка на Диске: **10 Декор-объекты**

Просто стоят и украшают: с ними ничего не делают (не ящики для лута).

**46. Стопка коробок** — `prop_boxes.glb` · 80 × 90 см
```
Replace the bed with a neat stack of three cardboard boxes of different sizes, taped. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**47. Две бочки** — `prop_barrels.glb` · 120 × 90 см
```
Replace the bed with two grey metal drums standing side by side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**48. Мешки** — `prop_sacks.glb` · 90 × 50 см
```
Replace the bed with a small pile of three burlap sacks of grain. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**49. Газовые баллоны** — `prop_gas.glb` · 60 × 110 см
```
Replace the bed with two tall gas cylinders, one red and one green, chained together. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**50. Цветок в горшке** — `prop_plant.glb` · 40 × 60 см
```
Replace the bed with a green leafy house plant in a clay pot, a little dry. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**51. Стопка книг** — `prop_books.glb` · 40 × 30 см
```
Replace the bed with a stack of old books with colorful covers. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**52. Занавеска** — `prop_curtain.glb` · 120 × 200 см
```
Replace the bed with a simple beige cloth curtain hanging from a thin metal rod, slightly pulled to one side. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**53. Верёвка с бельём** — `prop_laundry.glb` · 200 × 60 см
```
Replace the bed with a rope stretched horizontally with a few clothes and a towel hanging on it with clothespins. Keep exactly the same art style, level of detail, lighting and dark background as the original image, but show it straight from the front, flat, centered. Use its own natural colors, soft and clean, slightly worn. Nothing else in the picture, no text.
```

**54. Кресло** — `prop_armchair.glb` · 80 × 90 см
```
Replace the bed with an old cozy armchair with red fabric upholstery, a little worn. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

**55. Тележка** — `prop_cart.glb` · 80 × 90 см
```
Replace the bed with a small four-wheel metal hand cart with a wooden crate on it. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; soft, clean and slightly worn, add rust only where it really makes sense. Single object, no text.
```

## 8. Фоны-панорамы (картинки)

Папка на Диске: **14 Прочее**

Фон за улицей: игра повторяет его по ширине и двигает медленнее переднего плана. Делать **генератором картинок**
(тот же образец-кровать → ✏️, или просто «Изображение»), формат **самый широкий** (лучше 3:1, можно 16:9 — подрежу).
Сохранить **PNG**, имя — как в списке. Края подгоню, чтобы шва не было.

**56. Пустошь со скалами (трасса)** — `pano_wasteland.png`
```
Replace the whole picture with a dry wasteland with distant rocky mesas, a few dead trees and broken power poles. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

**57. Пригород** — `pano_suburb.png`
```
Replace the whole picture with abandoned suburban houses with broken roofs, fences, a few bare trees and a water tower in the distance. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

**58. Городок** — `pano_town.png`
```
Replace the whole picture with a small ruined town with low brick buildings, shop signs without text, a church tower and street lamps. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

**59. Руины города** — `pano_ruins.png`
```
Replace the whole picture with a ruined city skyline with broken high-rise buildings, cranes and smoke in the far distance. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

**60. Лес** — `pano_forest.png`
```
Replace the whole picture with an overgrown pine forest edge with a few abandoned cabins. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

**61. Лагерь** — `pano_camp.png`
```
Replace the whole picture with a scrap-metal survivor camp with walls of rusty sheets, watchtowers and tents. Same soft stylized low poly painted art style as the original image: simple shapes, soft gradients, gentle dusk light, muted cool blue-grey palette with a few warm accents. Wide panoramic landscape, side view, flat horizon, the ground line straight and horizontal at about 85 % of the image height, nothing in the foreground, no people, no text. The left and right edges must match so the picture can repeat seamlessly.
```

## Что делает игра

- Основы стен кусками в ряд и **красит** в цвет комнаты; линии — на всю ширину; вертикальное и декор — между ними,
  случайно, но одинаково при каждом запуске; пол — настил/ковры в части комнат; лампы светят своим цветом.
- Настройки — `data/config/view3d.json` → `wall_kit` (какие куски в каких комнатах).
