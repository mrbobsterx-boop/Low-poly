# Партия 2026-10-14 — улица, природа, поезд, плот, лук

Просьба автора (2026-10-14): деревья (3 обычных + 2 сухих — для плохих локаций), «островки» мелочей для улицы,
поезд на рельсы (тепловоз, пассажирский вагон, грузовой), плот, лук. Кусты у воды и стрелы — **нарисованы
кодом** (`tools/make_props.py`, в Tripo не нужны).

**Как делать (решение автора 2026-10-14):** образец стиля — **ёлка** (`docs/ref/style_tree_sample.webp`), не кровать.
Загрузить картинку ёлки → вставить запрос → картинка → 3D. В запросах нет «Replace / замени» (с ним Tripo переделывал
образец), а есть «exactly the same art style» — каждый запрос **целиком**, копировать один блок. Готовый GLB — в папку Диска из таблицы, имя файла — из таблицы (`<имя>.glb`).

**Обработка (второй чат):** `tools/tripo_process.py`, имена — без `_вариант` (декор, не объекты ОС). Размер — по
таблице: деревья и вагоны — длинные/высокие, см. колонку «по чему мерить». Перед — к −Y (у вагонов и плота — **длинной
стороной вдоль X**, к камере боком).

---

## 1. Деревья (папка Диска «14 Природа»)

| № | Файл | Размер | По чему мерить |
|---|---|---|---|
| 1 | `tree_oak` | 4,5 × 5,5 м | высота |
| 2 | `tree_birch` | 2,5 × 6 м | высота |
| 3 | `tree_maple` | 3,5 × 5 м | высота |
| 4 | `tree_dead_bare` | 3 × 5 м | высота |
| 5 | `tree_dead_burnt` | 2 × 4 м | высота |

**1. Дуб** — `tree_oak.glb`
```
A big old oak tree with a thick trunk, wide round crown of dark green leaves and visible roots. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

**2. Берёза** — `tree_birch.glb`
```
A tall slim birch tree with a white trunk with black marks and a light green airy crown. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

**3. Клён** — `tree_maple.glb`
```
A maple tree with a straight brown trunk and a full rounded crown of green and slightly orange leaves. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

**4. Сухое дерево** — `tree_dead_bare.glb`
```
A dead dry tree without leaves, grey cracked bark, twisted bare branches, a few broken branches. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

**5. Обгоревшее дерево** — `tree_dead_burnt.glb`
```
A burnt dead tree: black charred trunk broken at the top, a few short burnt branches, no leaves, ash at the roots. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

## 2. Островки мелочей для улицы (папка «15 Улица — островки»)

Каждый островок — **одна модель из нескольких вещей рядом** (поставил — и уголок улицы готов). Размер — по ширине.

| № | Файл | Что | Ширина |
|---|---|---|---|
| 6 | `isle_trash_bins` | 2 маленьких урны, мешки, бумажки | 1,6 м |
| 7 | `isle_dumpster` | мусорный контейнер, мешки, коробки | 2,6 м |
| 8 | `isle_fence_tires` | кусок забора, покрышки, сорняки | 2,4 м |
| 9 | `isle_bench_bin` | скамейка, урна, газеты | 2,2 м |
| 10 | `isle_hydrant` | гидрант, конус, знак | 1,4 м |
| 11 | `isle_mailbox` | почтовый ящик, газетный автомат, коробка | 1,6 м |
| 12 | `isle_bikes` | стойка с 2 старыми велосипедами | 2,0 м |
| 13 | `isle_pallets` | поддоны, ящики, брезент | 2,2 м |
| 14 | `isle_roadworks` | ограждения, конусы, куча песка, лопата | 2,6 м |
| 15 | `isle_scrap` | куча металлолома, дверь машины, бочка | 2,4 м |
| 16 | `isle_planter` | бетонная клумба с сухими цветами, урна | 1,8 м |
| 17 | `isle_barrels_fire` | бочка с костром, ящики-сиденья, кастрюля | 1,8 м |

**6. 2 маленьких урны, мешки, бумажки** — `isle_trash_bins.glb`
```
Two small metal street trash bins standing side by side, a few black garbage bags and crumpled papers on the ground around them. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**7. мусорный контейнер, мешки, коробки** — `isle_dumpster.glb`
```
A green metal dumpster with a half-open lid, black garbage bags and flattened cardboard boxes piled next to it. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**8. кусок забора, покрышки, сорняки** — `isle_fence_tires.glb`
```
A short broken wooden fence section, a stack of three old car tires in front of it and tall weeds growing around. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**9. скамейка, урна, газеты** — `isle_bench_bin.glb`
```
An old wooden park bench, a small metal trash bin next to it and a few old newspapers on the ground. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**10. гидрант, конус, знак** — `isle_hydrant.glb`
```
A red fire hydrant, an orange traffic cone lying beside it and a small bent street sign on a pole. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**11. почтовый ящик, газетный автомат, коробка** — `isle_mailbox.glb`
```
A blue street mailbox, a rusty newspaper vending box and a soggy cardboard box next to them. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**12. стойка с 2 старыми велосипедами** — `isle_bikes.glb`
```
A metal bicycle rack with two old rusty bicycles leaning in it, one with a flat tire. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**13. поддоны, ящики, брезент** — `isle_pallets.glb`
```
Two stacked wooden pallets, a few wooden crates and a torn blue tarp half covering them. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**14. ограждения, конусы, куча песка, лопата** — `isle_roadworks.glb`
```
Road works: two striped road barriers, three traffic cones, a small pile of sand with a shovel stuck in it. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**15. куча металлолома, дверь машины, бочка** — `isle_scrap.glb`
```
A pile of scrap metal: bent pipes, sheets of metal, an old car door and a rusty barrel. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**16. бетонная клумба с сухими цветами, урна** — `isle_planter.glb`
```
A square concrete street planter with dry dead flowers and a small trash bin next to it. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

**17. бочка с костром, ящики-сиденья, кастрюля** — `isle_barrels_fire.glb`
```
A rusty metal barrel with a small fire burning inside, two wooden crates used as seats and an old cooking pot. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the objects' own natural colors; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

## 3. Поезд (папка «16 Поезд»)

Рельсы в игре — `mine_rails_straight` (кусок 3 м, ширина колеи ≈ 1,2 м). Вагоны — узкоколейные, **колёса по колее**,
снизу без рельсов. Сбоку (длинной стороной к камере) — так их видно в разрезе мира.

| № | Файл | Что | Размер (длина × высота) |
|---|---|---|---|
| 18 | `train_loco_diesel` | тепловоз (± современный, не паровоз — решение автора) | 7 × 3 м |
| 19 | `train_coach` | пассажирский вагон (± современный; один на оба — решение автора) | 8 × 2,8 м |
| 21 | `train_freight` | грузовой вагон (крытый, дверь-купе) | 7 × 2,7 м |

**18. тепловоз (± современный, не паровоз — решение автора)** — `train_loco_diesel.glb`
```
A fairly modern diesel locomotive from the late 20th century: boxy steel body with a driver's cab with big front windows at one end, side walkways with yellow handrails, roof vents and exhaust, faded red and grey paint with a yellow stripe, dirty and slightly rusty, compact size for a narrow-gauge railway. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the object's own natural colors; add rust and wear where it makes sense. Side view, long side facing the camera. Single object, no rails, no ground, no text.
```

**19. пассажирский вагон (± современный)** — `train_coach.glb`
```
A fairly modern passenger railway car from the late 20th century: long smooth steel body with a row of big rectangular windows, sliding doors near both ends, a rounded roof with vents, rubber gangway connectors at both ends, two wheel bogies underneath, dirty and worn, compact size for a narrow-gauge railway. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the object's own natural colors; add rust and wear where it makes sense. Side view, long side facing the camera. Single object, no rails, no ground, no text.
```


**21. грузовой вагон (крытый, дверь-купе)** — `train_freight.glb`
```
A closed railway boxcar: a tall rectangular wooden box on wheels with four solid plank walls and a curved metal roof, fully enclosed like a big wooden container, a large sliding door in the middle of the long side, a rusty metal frame, two wheel bogies underneath, a ladder at one end. It is not a flatcar and not an open platform. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Use the object's own natural colors; add rust and wear where it makes sense. Side view, long side facing the camera. Single object, no rails, no ground, no text.
```

## 4. Плот (папка «14 Природа»)

| № | Файл | Размер |
|---|---|---|
| 22 | `raft_logs` | 3 × 2 м (по длине) |

```
A simple survival raft made of logs tied together with ropes, a wooden paddle lying on top and a small crate, seen slightly from above. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no water, no text.
```

## 5. Лук (папка «14 Природа» или «Оружие»)

В игре уже есть `weapon_bow_ohotnichiy` (лук **со стрелами** — модель объекта «Лук»). Этот — **лук отдельно, без
стрел**, чтобы держать в руке и стрелять (стрелы — отдельной моделью `arrow_wood`, уже нарисованы).

| № | Файл | Размер |
|---|---|---|
| 23 | `bow_wood_simple` | 1,2 м (по высоте, лук стоит вертикально) |

```
A simple wooden recurve bow standing upright, with a leather grip in the middle and a taut string, without any arrows, no quiver. Exactly the same art style as the reference image: stylized low poly with hand-painted textures, chunky soft shapes, the same level of detail, the same warm lighting, the same camera angle and the same plain dark background. Use the reference image only for the style. Single object, no text.
```

---

## Нарисовано кодом (`tools/make_props.py`, уже в `export/`)

| Файл | Что | Размер |
|---|---|---|
| `bush_water_reeds` | камыш с рогозом (коричневые «початки») на кочке | 1,2 × 1,6 м |
| `bush_willow` | куст ивы со свисающими прядями | 1,2 × 1,4 м |
| `bush_water_sedge` | осока с мокрыми камнями | 0,9 × 0,7 м |
| `arrow_wood` | стрела 75 см (лежит вдоль X) | 0,76 м |
| `arrows_bundle` | пучок из 6 стрел, перевязан бечёвкой | 0,76 м (высота) |
