# Партия 2026-10-14 — улица, природа, поезд, плот, лук

Просьба автора (2026-10-14): деревья (3 обычных + 2 сухих — для плохих локаций), «островки» мелочей для улицы,
поезд на рельсы (паровоз на угле, 2 пассажирских вагона, грузовой), плот, лук. Кусты у воды и стрелы — **нарисованы
кодом** (`tools/make_props.py`, в Tripo не нужны).

**Как делать (как все объекты, `TRIPO_OBJECTS.md`):** загрузить картинку кровати-образца → вставить запрос → картинка
→ 3D. Готовый GLB — в папку Диска из таблицы, имя файла — из таблицы (`<имя>.glb`).

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
Replace the bed with a big old oak tree with a thick trunk, wide round crown of dark green leaves and visible roots. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
```

**2. Берёза** — `tree_birch.glb`
```
Replace the bed with a tall slim birch tree with a white trunk with black marks and a light green airy crown. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
```

**3. Клён** — `tree_maple.glb`
```
Replace the bed with a maple tree with a straight brown trunk and a full rounded crown of green and slightly orange leaves. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
```

**4. Сухое дерево** — `tree_dead_bare.glb`
```
Replace the bed with a dead dry tree without leaves, grey cracked bark, twisted bare branches, a few broken branches. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
```

**5. Обгоревшее дерево** — `tree_dead_burnt.glb`
```
Replace the bed with a burnt dead tree: black charred trunk broken at the top, a few short burnt branches, no leaves, ash at the roots. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
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

Общий хвост запроса (вставлять после описания):
```
Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the objects' own natural colors and materials, not the colors of the bed; add rust, dirt and wear where it makes sense. A small group of objects standing close together on the ground, no ground plate, no text.
```

- **6.** `Replace the bed with two small metal street trash bins standing side by side, a few black garbage bags and crumpled papers on the ground around them.`
- **7.** `Replace the bed with a green metal dumpster with a half-open lid, black garbage bags and flattened cardboard boxes piled next to it.`
- **8.** `Replace the bed with a short broken wooden fence section, a stack of three old car tires in front of it and tall weeds growing around.`
- **9.** `Replace the bed with an old wooden park bench, a small metal trash bin next to it and a few old newspapers on the ground.`
- **10.** `Replace the bed with a red fire hydrant, an orange traffic cone lying beside it and a small bent street sign on a pole.`
- **11.** `Replace the bed with a blue street mailbox, a rusty newspaper vending box and a soggy cardboard box next to them.`
- **12.** `Replace the bed with a metal bicycle rack with two old rusty bicycles leaning in it, one with a flat tire.`
- **13.** `Replace the bed with two stacked wooden pallets, a few wooden crates and a torn blue tarp half covering them.`
- **14.** `Replace the bed with road works: two striped road barriers, three traffic cones, a small pile of sand with a shovel stuck in it.`
- **15.** `Replace the bed with a pile of scrap metal: bent pipes, sheets of metal, an old car door and a rusty barrel.`
- **16.** `Replace the bed with a square concrete street planter with dry dead flowers and a small trash bin next to it.`
- **17.** `Replace the bed with a rusty metal barrel with a small fire burning inside, two wooden crates used as seats and an old cooking pot.`

## 3. Поезд (папка «16 Поезд»)

Рельсы в игре — `mine_rails_straight` (кусок 3 м, ширина колеи ≈ 1,2 м). Вагоны — узкоколейные, **колёса по колее**,
снизу без рельсов. Сбоку (длинной стороной к камере) — так их видно в разрезе мира.

| № | Файл | Что | Размер (длина × высота) |
|---|---|---|---|
| 18 | `train_loco_steam` | паровоз на угле (с тендером) | 7 × 3 м |
| 19 | `train_coach_a` | пассажирский вагон, зелёный | 8 × 2,8 м |
| 20 | `train_coach_b` | пассажирский вагон, бордовый, потрёпанный | 8 × 2,8 м |
| 21 | `train_freight` | грузовой вагон (крытый, дверь-купе) | 7 × 2,7 м |

Хвост запроса:
```
Side view, long side facing the camera. Keep exactly the same art style, level of detail, lighting and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear where it makes sense. Single object, no rails, no ground, no text.
```

- **18.** `Replace the bed with a small old narrow-gauge steam locomotive that runs on coal: black boiler, tall chimney, driver's cab and a small coal tender attached behind, red wheels.`
- **19.** `Replace the bed with an old narrow-gauge wooden passenger railway car painted green, with a row of windows, doors at both ends and small platforms with railings.`
- **20.** `Replace the bed with an old narrow-gauge passenger railway car painted dark red, faded paint, a few boarded-up windows, doors at both ends.`
- **21.** `Replace the bed with an old narrow-gauge covered freight railway wagon made of wooden planks with a big sliding door in the middle, rusty metal frame.`

## 4. Плот (папка «14 Природа»)

| № | Файл | Размер |
|---|---|---|
| 22 | `raft_logs` | 3 × 2 м (по длине) |

```
Replace the bed with a simple survival raft made of logs tied together with ropes, a wooden paddle lying on top and a small crate. Seen slightly from above. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no water, no text.
```

## 5. Лук (папка «14 Природа» или «Оружие»)

В игре уже есть `weapon_bow_ohotnichiy` (лук **со стрелами** — модель объекта «Лук»). Этот — **лук отдельно, без
стрел**, чтобы держать в руке и стрелять (стрелы — отдельной моделью `arrow_wood`, уже нарисованы).

| № | Файл | Размер |
|---|---|---|
| 23 | `bow_wood_simple` | 1,2 м (по высоте, лук стоит вертикально) |

```
Replace the bed with a simple wooden recurve bow standing upright, with a leather grip in the middle and a taut string, without any arrows, no quiver. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed. Single object, no text.
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
