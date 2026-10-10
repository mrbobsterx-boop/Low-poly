# План всех объектов — стиль «кровать-образец» (low poly, нарисованный)

Решение автора (2026-10-10): все объекты — **в одном стиле**, как кровать-образец (`bed_single`), но **разные**:
у каждого свои цвета и материалы, ржавчина и потёртости — только там, где уместно.

## Как делать (Tripo)

1. **Модель → картинка-образец:** загрузить снимок кровати-образца (тёмный фон).
2. Под картинкой — **✏️ (карандаш)** → вставить запрос предмета из списка ниже (один серый блок) → получится
   **картинка** этого предмета в том же стиле. Не похоже — повторить.
3. Картинка удалась → **«Создать»** (HD модель) → 3D-модель.
4. Скачать **GLB**, назвать **как в списке** (`имя файла`), положить в **папку на Диске** из заголовка раздела.
5. Пачка готова → написать чату игры «забери <папка>».

Размер — ширина × высота, см (из ОС): точный размер выставит обработка. Кровати, верстаки, столы разборки, швейные
столы, ванна, койка, стойка — подгоняются по ширине, остальное — по высоте.

**Не делаем:** блоки грунта (земля, камень, бетон…) — их рисует игра; пятно крови — тоже игра. Сломанные / открытые
варианты — показывает игра. **Сначала по одному варианту** на объект (в списке — какой).

**Порядок:** разделы 1–7 (то, что стоит в мире) → 8 → 9 → 10 (персонажам нужен риг — отдельно).

---

## 1. Мебель

Папка на Диске: **05 Мебель**

**1. Кровать** (Железная койка) — `bed_single_zheleznaya_koyka.glb` · 200 × 60 см — **это и есть образец**: можно положить готовую модель кровати-образца, запрос — если нужна другая
```
Replace the bed with a single metal frame bed with a thin mattress, a pillow and a folded wool blanket. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**2. Двухъярусная койка** (Металлическая) — `bunk_bed_metallicheskaya.glb` · 200 × 180 см
```
Replace the bed with a metal bunk bed with two levels, two thin mattresses, pillows and a small ladder on the side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**3. Стол** (Обеденный) — `table_wood_obedennyy.glb` · 120 × 75 см
```
Replace the bed with a simple wooden dining table with four straight legs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**4. Стул** (Деревянный) — `chair_wood_derevyannyy.glb` · 45 × 90 см
```
Replace the bed with a simple wooden chair with a straight back. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**5. Унитаз** (Фаянсовый со смывом) — `toilet_fayansovyy_so_smyvom.glb` · 40 × 75 см
```
Replace the bed with a white ceramic toilet with a tank and a lid. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**6. Раковина с краном** (Кухонная) — `sink_tap_kuhonnaya.glb` · 80 × 90 см
```
Replace the bed with a kitchen sink with a metal tap on a small wooden cabinet. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**7. Ванна** (Чугунная) — `bathtub_chugunnaya.glb` · 170 × 60 см
```
Replace the bed with an old cast iron bathtub on four small legs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**8. Медицинская койка** (Складная) — `cot_medical_skladnaya.glb` · 190 × 80 см
```
Replace the bed with a folding medical cot with a metal frame and a canvas bed. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**9. Грядка** (Деревянный ящик) — `planter_box_derevyannyy_yaschik.glb` · 120 × 40 см
```
Replace the bed with a long wooden planter box filled with soil and small green sprouts. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**10. Торговый прилавок** (Прилавок) — `trade_stall_prilavok.glb` · 160 × 110 см
```
Replace the bed with a market trade stall with a wooden counter, a cloth canopy and goods on it. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 2. Верстаки

Папка на Диске: **06 Верстаки**

**11. Верстак** (Деревянный базовый) — `workbench_basic_derevyannyy_bazovyy.glb` · 160 × 95 см
```
Replace the bed with a workbench: a flat wooden top on a straight square metal tube frame with hex bolts, a metal vise on one corner, a low shelf underneath and a few tools hanging on a small back board. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**12. Электронный верстак** (Настольный) — `workbench_electronics_nastolnyy.glb` · 140 × 95 см
```
Replace the bed with an electronics workbench: a desk with a pegboard of small tools, a soldering iron, a multimeter, a small screen and boxes of parts. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**13. Стол разборки** (Ручной) — `recycler_bench_ruchnoy.glb` · 130 × 95 см
```
Replace the bed with a disassembly table: a heavy metal table with a vise, a crowbar, scrap parts and bins underneath. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**14. Швейный стол** (Ручная машина) — `sewing_table_ruchnaya_mashina.glb` · 110 × 85 см
```
Replace the bed with a sewing table with a hand-cranked sewing machine, fabric rolls and a small drawer. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 3. Контейнеры (шкафы, ящики, хранилища)

Папка на Диске: **07 Контейнеры (ящики, шкафы, хранилища)**

**15. Шкаф** (Деревянный двустворчатый) — `wardrobe_derevyannyy_dvustvorchatyy.glb` · 100 × 200 см
```
Replace the bed with a tall wooden wardrobe with two doors, simple handles and small legs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**16. Полка** (Деревянная) — `shelf_wood_derevyannaya.glb` · 100 × 30 см
```
Replace the bed with a wooden wall shelf on two metal brackets with a few jars and cans on it, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**17. Бочка для воды** (Пластиковая 200 л) — `barrel_water_plastikovaya_200_l.glb` · 60 × 90 см
```
Replace the bed with a blue plastic water barrel with a lid and a tap near the bottom. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**18. Резервуар воды** (Пластиковый 1000 л) — `tank_water_plastikovyy_1000_l.glb` · 160 × 190 см
```
Replace the bed with a large plastic water tank of 1000 liters inside a metal cage frame with a tap. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**19. Аккумулятор** (Автомобильный 12 В) — `battery_bank_avtomobilnyy_12_v.glb` · 60 × 40 см
```
Replace the bed with a large 12 volt car battery with two terminals and a carrying handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**20. Канистра с топливом** (5 л) — `fuel_canister_5_l.glb` · 35 × 45 см
```
Replace the bed with a metal jerry can for fuel with a handle and a cap. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**21. Кухонная тумба** (С раковиной) — `kitchen_counter_s_rakovinoy.glb` · 120 × 90 см
```
Replace the bed with a kitchen counter cabinet with a sink, two doors and a drawer. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**22. Аптечка** (Домашняя) — `first_aid_kit_domashnyaya.glb` · 25 × 18 см
```
Replace the bed with a white first aid box with a red cross and a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**23. Аптечный шкафчик** (Ванный) — `medicine_cabinet_vannyy.glb` · 50 × 60 см
```
Replace the bed with a small wall-mounted medicine cabinet with a mirror door and a red cross, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**24. Деревянный ящик** (Малый) — `crate_wood_malyy.glb` · 60 × 50 см
```
Replace the bed with a small wooden supply crate with metal corners. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**25. Стеллаж металлический** (С 3 полками) — `rack_metal_s_3_polkami.glb` · 120 × 200 см
```
Replace the bed with a tall metal storage rack with three shelves holding a few boxes. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**26. Шкафчик металлический** (Спортивный) — `locker_metal_sportivnyy.glb` · 50 × 180 см
```
Replace the bed with a tall narrow metal locker with vent slots and a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**27. Сейф** (Настенный) — `safe_metal_nastennyy.glb` · 50 × 60 см
```
Replace the bed with a heavy steel safe with a round dial and a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**28. Ящик с инструментами** (Пластиковый) — `toolbox_plastikovyy.glb` · 40 × 25 см
```
Replace the bed with a plastic toolbox with a handle and latches. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**29. Мусорный бак** (Зелёный) — `dumpster_zelenyy.glb` · 130 × 110 см
```
Replace the bed with a green metal dumpster with a lid. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**30. Склад фракции** (Ящики) — `faction_stockpile_yaschiki.glb` · 200 × 120 см
```
Replace the bed with a stockpile of stacked wooden crates and barrels under a tarp. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 4. Техника и машины

Папка на Диске: **08 Техника и машины**

**31. Лампа потолочная** (Лампа накаливания) — `lamp_ceiling_lampa_nakalivaniya.glb` · 30 × 25 см
```
Replace the bed with a hanging ceiling lamp with a metal shade and a single bulb on a short cord. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**32. Радиоприёмник** (Настольный) — `radio_desk_nastolnyy.glb` · 35 × 25 см
```
Replace the bed with an old tabletop tube radio with a speaker grille, two knobs and a dial. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**33. Печь-буржуйка** (Стальная бочка) — `stove_heat_stalnaya_bochka.glb` · 60 × 90 см
```
Replace the bed with a small wood-burning stove made from a steel barrel with a little door, short legs and a chimney pipe going up. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**34. Дождеуловитель** (Плёнка и желоб) — `rain_collector_plenka_i_zhelob.glb` · 110 × 60 см
```
Replace the bed with a rain collector made from a stretched plastic sheet on a wooden frame with a gutter and a barrel. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**35. Насос** (Ручной рычажный) — `water_pump_ruchnoy_rychazhnyy.glb` · 50 × 60 см
```
Replace the bed with a manual hand lever water pump made of cast iron on a short pipe. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**36. Очиститель воды** (Керамический фильтр) — `water_purifier_keramicheskiy_filtr.glb` · 60 × 100 см
```
Replace the bed with a water purifier with a ceramic filter: two stacked metal containers with a tap on the bottom one. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**37. Солнечная панель** (Малая 100 Вт) — `solar_panel_malaya_100_vt.glb` · 120 × 80 см
```
Replace the bed with a small solar panel on a metal stand, tilted towards the sky. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**38. Ветрогенератор** (Малый горизонтальный) — `wind_turbine_malyy_gorizontalnyy.glb` · 100 × 300 см
```
Replace the bed with a small wind turbine with three blades on a tall metal pole with guy wires. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**39. Велогенератор** (Стационарный) — `bike_generator_statsionarnyy.glb` · 120 × 110 см
```
Replace the bed with a stationary bicycle connected to a small electric generator with a belt. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**40. Беговая дорожка-генератор** (Беговая дорожка) — `treadmill_generator_begovaya_dorozhka.glb` · 160 × 120 см
```
Replace the bed with an old treadmill connected to an electric generator with wires. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**41. Генератор на топливе** (Портативный) — `fuel_generator_portativnyy.glb` · 70 × 60 см
```
Replace the bed with a portable fuel generator in a metal tube frame with a pull starter. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**42. Холодильник** (Электрический) — `fridge_elektricheskiy.glb` · 70 × 180 см
```
Replace the bed with an old tall rounded refrigerator with a chrome handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**43. Лампа для урожая** (Фиолетовая LED) — `grow_lamp_fioletovaya_led.glb` · 80 × 15 см
```
Replace the bed with a long hanging LED grow lamp panel glowing purple on two chains. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**44. Панель убежища** (Простой пульт) — `shelter_panel_prostoy_pult.glb` · 60 × 70 см
```
Replace the bed with a wall-mounted shelter control panel with switches, lamps and a small gauge, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**45. Выключатель** (Клавишный) — `light_switch_klavishnyy.glb` · 8 × 12 см
```
Replace the bed with a simple wall light switch on a small plate, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**46. Электрощит** (Бытовой) — `fuse_box_bytovoy.glb` · 40 × 50 см
```
Replace the bed with a wall-mounted metal fuse box with a small door and cables going out, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**47. Плита** (Газовая) — `stove_cook_gazovaya.glb` · 70 × 90 см
```
Replace the bed with an old gas kitchen stove with four burners, knobs and an oven door. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**48. Костёр** (Простой) — `campfire_prostoy.glb` · 80 × 50 см
```
Replace the bed with a campfire with logs in a ring of stones and small flames. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**49. Гидропонная стойка** (Малая) — `hydro_rack_malaya.glb` · 100 × 180 см
```
Replace the bed with a hydroponic rack with three shelves of plants in trays, tubes and purple grow lights. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**50. Брошенная машина** (Седан) — `car_abandoned_sedan.glb` · 450 × 160 см
```
Replace the bed with an abandoned old sedan car with flat tyres and dust. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 5. Двери и строительное

Папка на Диске: **09 Строительное и двери**

**51. Водонапорная башня** (Кирпичная) — `water_tower_kirpichnaya.glb` · 400 × 1000 см
```
Replace the bed with a tall brick water tower with a round tank on top and a small door at the bottom. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**52. Дверь деревянная** (Внутренняя) — `door_wood_vnutrennyaya.glb` · 100 × 200 см
```
Replace the bed with an interior wooden door in a wooden frame with a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**53. Дверь металлическая** (Стальная) — `door_metal_stalnaya.glb` · 100 × 200 см
```
Replace the bed with a heavy steel door in a metal frame with rivets and a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**54. Люк бункера** (Люк с колесом) — `hatch_bunker_lyuk_s_kolesom.glb` · 100 × 60 см
```
Replace the bed with a round steel bunker hatch with a wheel handle in a frame. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**55. Окно** (Целое) — `window_basic_tseloe.glb` · 100 × 100 см
```
Replace the bed with a wooden window frame with glass panes. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**56. Лестница** (Деревянная) — `stairs_wood_derevyannaya.glb` · 110 × 260 см
```
Replace the bed with a wooden staircase with a handrail. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**57. Металлическая лестница** (Пристенная) — `ladder_metal_pristennaya.glb` · 50 × 300 см
```
Replace the bed with a tall metal wall ladder. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**58. Баррикада** (Доски на окне) — `barricade_planks_doski_na_okne.glb` · 110 × 200 см
```
Replace the bed with a barricade of wooden planks nailed across a window frame. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**59. Забор с колючей проволокой** (Сетка) — `fence_wire_setka.glb` · 200 × 150 см
```
Replace the bed with a fence section of wire mesh on metal posts with barbed wire on top. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**60. Палатка** (Одноместная) — `tent_camp_odnomestnaya.glb` · 220 × 140 см
```
Replace the bed with a small one-person camping tent. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**61. Указатель развилки** (Дорожный знак) — `signpost_fork_dorozhnyy_znak.glb` · 80 × 220 см
```
Replace the bed with a road signpost with two arrow signs without letters on a metal pole. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**62. Наблюдательная вышка** (Деревянная) — `watchtower_derevyannaya.glb` · 200 × 500 см
```
Replace the bed with a tall wooden watchtower with a ladder and a small roofed platform. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 6. Улица и декор

Папка на Диске: **10 Декор-объекты**

**63. Часы настенные** (Механические) — `clock_wall_mehanicheskie.glb` · 30 × 30 см
```
Replace the bed with a round wall clock with a metal rim and simple hands, flat back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**64. Колодец / скважина** (Ручной колодец с воротом) — `well_hand_ruchnoy_kolodets_s_vorotom.glb` · 90 × 130 см
```
Replace the bed with a small stone well with a wooden roof, a crank and a rope with a bucket. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**65. Остов сгоревшей машины** (Разобранная) — `car_wreck_razobrannaya.glb` · 450 × 150 см
```
Replace the bed with a burnt out car wreck without wheels and doors. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**66. Уличный фонарь** (Целый) — `street_lamp_tselyy.glb` · 30 × 400 см
```
Replace the bed with a tall street lamp on a metal pole. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**67. Рекламный щит** (Целый) — `billboard_road_tselyy.glb` · 150 × 400 см
```
Replace the bed with a roadside billboard on two metal legs with a faded blank poster. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**68. Куча хлама** (Металлолом) — `scrap_pile_metallolom.glb` · 120 × 80 см
```
Replace the bed with a pile of scrap: metal sheets, pipes, tyres and wooden boards. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**69. Скамейка** (Деревянная) — `bench_street_derevyannaya.glb` · 150 × 80 см
```
Replace the bed with a wooden park bench with metal legs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**70. Могила** (Холм) — `grave_mound_holm.glb` · 150 × 60 см
```
Replace the bed with a grave mound of earth with a wooden cross. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**71. Погребальный костёр** (Костёр) — `pyre_pile_koster.glb` · 150 × 80 см
```
Replace the bed with a funeral pyre of stacked logs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**72. Знамя фракции** (Знамя) — `faction_banner_znamya.glb` · 60 × 200 см
```
Replace the bed with a tall pole with a hanging cloth banner with a simple symbol. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**73. Доска объявлений** (Деревянная) — `noticeboard_derevyannaya.glb` · 100 × 80 см
```
Replace the bed with a wooden notice board on two legs with pinned paper notes without text. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 7. Растения

Папка на Диске: **11 Растения и точки ресурсов**

**74. Картофель (растение)** (Картофель) — `plant_potato_kartofel.glb` · 40 × 40 см
```
Replace the bed with a potato plant bush in soil. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**75. Пшеница (растение)** (Пшеница) — `plant_wheat_pshenitsa.glb` · 50 × 80 см
```
Replace the bed with a small patch of golden wheat stalks. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**76. Дерево** (Сосна) — `plant_tree_sosna.glb` · 160 × 450 см
```
Replace the bed with a tall pine tree. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**77. Ягодный куст** (Малина) — `bush_berry_malina.glb` · 80 × 70 см
```
Replace the bed with a raspberry bush with red berries. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 8. Инструменты, оружие, одежда

Папка на Диске: **12 Предметы, инструменты, оружие, одежда**

**78. Ведро** (Металлическое) — `bucket_metallicheskoe.glb` · 30 × 30 см
```
Replace the bed with a metal bucket with a handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**79. Кастрюля / котелок** (Алюминиевая) — `cooking_pot_alyuminievaya.glb` · 25 × 20 см
```
Replace the bed with an aluminium cooking pot with a lid and two handles. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**80. Консервный нож** (Ручной) — `tool_can_opener_ruchnoy.glb` · 15 × 8 см
```
Replace the bed with a manual can opener. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**81. Рюкзак** (Школьный (малый)) — `backpack_shkolnyy.glb` · 35 × 45 см
```
Replace the bed with a small school backpack with two straps. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**82. Молоток** (Столярный) — `tool_hammer_stolyarnyy.glb` · 30 × 10 см
```
Replace the bed with a carpenter hammer with a wooden handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**83. Гаечный ключ** (Разводной) — `tool_wrench_razvodnoy.glb` · 30 × 8 см
```
Replace the bed with an adjustable wrench. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**84. Отвёртка** (Крестовая) — `tool_screwdriver_krestovaya.glb` · 20 × 4 см
```
Replace the bed with a screwdriver with a red handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**85. Пила** (Ножовка) — `tool_saw_nozhovka.glb` · 50 × 12 см
```
Replace the bed with a hand saw with a wooden handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**86. Топор** (Колун) — `tool_axe_kolun.glb` · 35 × 60 см
```
Replace the bed with a splitting axe with a long wooden handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**87. Кирка** (Стальная) — `tool_pickaxe_stalnaya.glb` · 35 × 60 см
```
Replace the bed with a steel pickaxe with a wooden handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**88. Лопата** (Штыковая) — `tool_shovel_shtykovaya.glb` · 30 × 110 см
```
Replace the bed with a spade shovel with a long wooden handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**89. Кувалда** (Малая) — `tool_sledge_malaya.glb` · 30 × 90 см
```
Replace the bed with a small sledgehammer. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**90. Лом** (Стальной) — `tool_crowbar_stalnoy.glb` · 70 × 8 см
```
Replace the bed with a steel crowbar. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**91. Отмычки** (Набор) — `tool_lockpick_nabor.glb` · 10 × 5 см
```
Replace the bed with a small set of lockpicks in a leather pouch. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**92. Фонарик** (Ручной) — `tool_flashlight_ruchnoy.glb` · 10 × 25 см
```
Replace the bed with a metal flashlight. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**93. Паяльник** (Сетевой) — `tool_soldering_setevoy.glb` · 25 × 5 см
```
Replace the bed with an electric soldering iron with a cord. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**94. Нож** (Кухонный) — `tool_knife_kuhonnyy.glb` · 25 × 5 см
```
Replace the bed with a kitchen knife. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**95. Бейсбольная бита** (Деревянная) — `weapon_bat_derevyannaya.glb` · 90 × 10 см
```
Replace the bed with a wooden baseball bat with tape on the handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**96. Труба-дубинка** (Стальная труба) — `weapon_pipe_stalnaya_truba.glb` · 80 × 8 см
```
Replace the bed with a steel pipe club with tape on the grip. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**97. Мачете** (Мачете) — `weapon_machete_machete.glb` · 70 × 8 см
```
Replace the bed with a machete with a black handle. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**98. Пистолет** (9 мм) — `weapon_pistol_9_mm.glb` · 20 × 14 см
```
Replace the bed with a 9 mm pistol. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**99. Дробовик** (Помповый) — `weapon_shotgun_pompovyy.glb` · 100 × 15 см
```
Replace the bed with a pump-action shotgun. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**100. Лук** (Охотничий) — `weapon_bow_ohotnichiy.glb` · 70 × 110 см
```
Replace the bed with a hunting bow with a few arrows. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**101. Капкан / ловушка** (Капкан) — `trap_bear_kapkan.glb` · 40 × 10 см
```
Replace the bed with a steel bear trap, open. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**102. Куртка** (Кожаная) — `cloth_jacket_kozhanaya.glb` · 50 × 70 см
```
Replace the bed with a leather jacket. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**103. Штаны** (Джинсы) — `cloth_pants_dzhinsy.glb` · 40 × 80 см
```
Replace the bed with a pair of blue jeans. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**104. Ботинки** (Кроссовки) — `cloth_boots_krossovki.glb` · 30 × 20 см
```
Replace the bed with a pair of sneakers. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**105. Перчатки** (Рабочие) — `cloth_gloves_rabochie.glb` · 20 × 15 см
```
Replace the bed with a pair of work gloves. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**106. Противогаз** (Военный) — `mask_gas_voennyy.glb` · 25 × 30 см
```
Replace the bed with a military gas mask with a filter. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**107. Бронежилет** (Самодельный) — `vest_armor_samodelnyy.glb` · 45 × 60 см
```
Replace the bed with a homemade armor vest with metal plates and straps. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 9. Мелкие предметы (потом — лежат на полу и в рюкзаке)

Папка на Диске: **12 Предметы, инструменты, оружие, одежда**

**108. Лампочка** (Накаливания) — `lightbulb_nakalivaniya.glb` · 6 × 12 см
```
Replace the bed with a single old incandescent light bulb. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**109. Таблетки для очистки воды** (Хлорные) — `water_tablets_hlornye.glb` · 6 × 10 см
```
Replace the bed with a small plastic tube of water purification tablets. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**110. Бутылка с водой** (Пластиковая 0,5 л) — `bottle_water_plastikovaya_0_5_l.glb` · 8 × 25 см
```
Replace the bed with a plastic water bottle half full. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**111. Провод / кабель** (Тонкий) — `power_cable_tonkiy.glb` · 20 × 20 см
```
Replace the bed with a coiled bundle of electric cable. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**112. Батарейка** (Одноразовая) — `battery_cell_odnorazovaya.glb` · 3 × 6 см
```
Replace the bed with a single AA battery. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**113. Дрова** (Поленья) — `fuel_firewood_polenya.glb` · 40 × 15 см
```
Replace the bed with a small pile of chopped firewood logs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**114. Консервы** (Тушёнка) — `food_canned_tushenka.glb` · 8 × 10 см
```
Replace the bed with a tin can of stewed meat with a paper label without letters. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**115. Хлеб / сухари** (Хлеб) — `food_bread_hleb.glb` · 20 × 10 см
```
Replace the bed with a loaf of bread and a few dry crackers. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**116. Зерно** (Пшеница) — `food_grain_pshenitsa.glb` · 15 × 15 см
```
Replace the bed with a small burlap sack of wheat grain. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**117. Сырое мясо** (Кролик) — `meat_raw_krolik.glb` · 15 × 8 см
```
Replace the bed with a piece of raw meat. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**118. Приготовленное мясо** (Жареное) — `meat_cooked_zharenoe.glb` · 15 × 8 см
```
Replace the bed with a piece of roasted meat on a bone. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**119. Овощи (картофель, морковь)** (Картофель) — `veg_potato_kartofel.glb` · 8 × 8 см
```
Replace the bed with a few potatoes and carrots. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**120. Готовое блюдо (суп, рагу)** (Овощной суп) — `meal_soup_ovoschnoy_sup.glb` · 15 × 10 см
```
Replace the bed with a metal bowl of vegetable soup with a spoon. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**121. Сухпаёк** (Армейский) — `ration_dry_armeyskiy.glb` · 15 × 10 см
```
Replace the bed with an army dry ration pack in olive wrapping. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**122. Бинт** (Стерильный) — `bandage_sterilnyy.glb` · 10 × 6 см
```
Replace the bed with a rolled white bandage. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**123. Антисептик** (Спирт) — `antiseptic_spirt.glb` · 6 × 14 см
```
Replace the bed with a small glass bottle of antiseptic alcohol. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**124. Обезболивающее** (Таблетки) — `painkiller_tabletki.glb` · 6 × 8 см
```
Replace the bed with a small pill bottle of painkillers. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**125. Антибиотики** (Широкого спектра) — `antibiotics_shirokogo_spektra.glb` · 6 × 8 см
```
Replace the bed with a small box of antibiotic pills with a red cross mark. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**126. Шина** (Готовая) — `splint_gotovaya.glb` · 40 × 8 см
```
Replace the bed with a medical splint made of two flat boards and bandage. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**127. Медицинский набор** (Полевой) — `medical_kit_polevoy.glb` · 35 × 25 см
```
Replace the bed with a military field medical bag with a red cross patch. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**128. Яд** (Слабый) — `poison_vial_slabyy.glb` · 5 × 10 см
```
Replace the bed with a small glass vial with green poison liquid and a cork. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**129. Мыло** (Кусок мыла) — `soap_kusok_myla.glb` · 8 × 4 см
```
Replace the bed with a bar of soap. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**130. Семена** (Картофель) — `seed_bag_kartofel.glb` · 10 × 14 см
```
Replace the bed with a small paper bag of seeds. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**131. Удобрение** (Компост) — `fertilizer_bag_kompost.glb` · 25 × 35 см
```
Replace the bed with a sack of compost fertilizer. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**132. Доски** (Доска) — `mat_plank_doska.glb` · 100 × 10 см
```
Replace the bed with a stack of three wooden planks. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**133. Брёвна** (Полено) — `mat_log_poleno.glb` · 120 × 20 см
```
Replace the bed with a single wooden log. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**134. Металлолом** (Лом) — `mat_scrap_lom.glb` · 25 × 15 см
```
Replace the bed with a small pile of scrap metal pieces. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**135. Металлический лист** (Тонкий) — `mat_sheet_metal_tonkiy.glb` · 100 × 3 см
```
Replace the bed with a sheet of thin metal, slightly bent. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**136. Труба** (Стальная) — `mat_pipe_metal_stalnaya.glb` · 100 × 8 см
```
Replace the bed with a steel pipe section. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**137. Гвозди / крепёж** (Гвозди) — `mat_nails_gvozdi.glb` · 6 × 4 см
```
Replace the bed with a small pile of nails and bolts. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**138. Проволока / провод** (Медная) — `mat_wire_mednaya.glb` · 20 × 20 см
```
Replace the bed with a coil of copper wire. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**139. Ткань** (Лоскут) — `mat_cloth_loskut.glb` · 30 × 20 см
```
Replace the bed with a folded piece of cloth. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**140. Верёвка** (Пенька) — `mat_rope_penka.glb` · 30 × 10 см
```
Replace the bed with a coiled hemp rope. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**141. Цемент / стройматериалы** (Мешок цемента) — `mat_cement_meshok_tsementa.glb` · 30 × 40 см
```
Replace the bed with a paper sack of cement. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**142. Механические детали** (Шестерни) — `part_mech_shesterni.glb` · 15 × 15 см
```
Replace the bed with a small pile of gears and mechanical parts. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**143. Электронные компоненты** (Платы) — `part_electronic_platy.glb` · 10 × 10 см
```
Replace the bed with a few small circuit boards and electronic components. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**144. Редкая схема** (Военная плата) — `part_rare_circuit_voennaya_plata.glb` · 10 × 10 см
```
Replace the bed with a military circuit board with a shiny chip. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**145. Кусок камня** (Булыжник) — `stone_chunk_bulyzhnik.glb` · 15 × 12 см
```
Replace the bed with a rough chunk of stone. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**146. Грунт** (Чернозём) — `soil_clump_chernozem.glb` · 15 × 12 см
```
Replace the bed with a clump of dark soil. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**147. Железная руда** (Руда) — `iron_ore_ruda.glb` · 15 × 12 см
```
Replace the bed with a chunk of iron ore with rusty orange veins. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**148. Уголь** (Каменный) — `coal_chunk_kamennyy.glb` · 15 × 12 см
```
Replace the bed with a chunk of black coal. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**149. Строительный мусор** (Битый кирпич) — `mat_rubble_bityy_kirpich.glb` · 20 × 15 см
```
Replace the bed with a small pile of broken bricks. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**150. Стекло** (Лист стекла) — `mat_glass_list_stekla.glb` · 30 × 30 см
```
Replace the bed with a pane of glass. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**151. Ремонтный набор** (Малый набор) — `repair_kit_malyy_nabor.glb` · 25 × 15 см
```
Replace the bed with a small repair kit pouch with tools. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**152. Изолента / скотч** (Изолента) — `duct_tape_izolenta.glb` · 10 × 10 см
```
Replace the bed with a roll of grey duct tape. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**153. Навесной замок** (Навесной) — `lock_padlock_navesnoy.glb` · 6 × 10 см
```
Replace the bed with a metal padlock. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**154. Ключ** (Обычный) — `key_generic_obychnyy.glb` · 3 × 8 см
```
Replace the bed with a simple metal key. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**155. Патроны 9 мм** (Обычные) — `ammo_9mm_obychnye.glb` · 6 × 3 см
```
Replace the bed with a small box of 9 mm bullets. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**156. Патроны для дробовика** (Картечь) — `ammo_shells_kartech.glb` · 8 × 4 см
```
Replace the bed with a few red shotgun shells. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**157. Записка / дневник** (Записка) — `note_diary_zapiska.glb` · 15 × 20 см
```
Replace the bed with a worn notebook diary. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**158. Карта** (Карта района) — `map_paper_karta_rayona.glb` · 30 × 20 см
```
Replace the bed with a folded paper map. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

---

## 10. Персонажи, существа, останки (потом — после анимаций)

Папка на Диске: **13 Персонажи и существа (потом)**

**159. Выживший (шаблон)** (Игрок) — `survivor_base_igrok.glb` · 100 × 180 см
```
Replace the bed with a full body survivor character in a worn jumpsuit with a utility belt and boots, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**160. Зомби (ходячий)** (Ходячий) — `zombie_walker_hodyachiy.glb` · 100 × 180 см
```
Replace the bed with a full body slow zombie in torn clothes with grey skin, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**161. Зомби (быстрый)** (Бегун) — `zombie_runner_begun.glb` · 100 × 180 см
```
Replace the bed with a full body thin fast zombie in torn clothes, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**162. Зомби (тяжёлый)** (Здоровяк) — `zombie_brute_zdorovyak.glb` · 120 × 200 см
```
Replace the bed with a full body huge heavy zombie with big arms, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**163. Рейдер / бандит** (Мародёр) — `raider_human_maroder.glb` · 100 × 180 см
```
Replace the bed with a full body raider bandit character with a scarf over the face, leather jacket and spikes, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**164. Торговец** (Бродячий) — `trader_npc_brodyachiy.glb` · 100 × 180 см
```
Replace the bed with a full body wandering trader character with a big backpack full of goods, standing in a T-pose. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**165. Дикая собака** (Одиночная) — `dog_feral_odinochnaya.glb` · 90 × 60 см
```
Replace the bed with a feral dog, thin, standing on four legs. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**166. Кролик** (Кролик) — `rabbit_wild_krolik.glb` · 35 × 25 см
```
Replace the bed with a wild rabbit sitting. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**167. Крыса** (Крыса) — `rat_pest_krysa.glb` · 25 × 10 см
```
Replace the bed with a big rat. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**168. Мутант-ползун** (Ползун) — `mutant_crawler_polzun.glb` · 140 × 60 см
```
Replace the bed with a mutant crawler creature on all fours, long arms, grey skin. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**169. Останки человека** (Свежее) — `corpse_human_svezhee.glb` · 180 × 30 см
```
Replace the bed with human remains: a skeleton in torn clothes lying on the ground. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**170. Останки зомби** (Свежее) — `corpse_zombie_svezhee.glb` · 180 × 30 см
```
Replace the bed with zombie remains lying on the ground, torn clothes, grey skin. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```
