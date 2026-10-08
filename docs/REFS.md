# Картинки-образцы (референсы)

Взяты из ОС: `object-constructor/assets/refs/` (там 929 картинок). Сюда положено **по одной на объект**, уменьшено до 512 px,
имя файла = id: `docs/ref/<категория>/<id>.png`. Остальные варианты того же объекта — в колонке «Ещё в ОС»;
если нужен другой вариант — скажите, заменю.

**Картинки — только образец формы, пропорций и основного цвета.** Свет, тени, грязь, блики и мелкие детали с них
**не переносим** — см. правило 10 в `README.md` («чистая модель»).

Итого здесь: **124** объекта, из них ✅ 93, 🟡 31.

Сложность для low-poly модели скриптом:

- **✅ легко** — из коробок и цилиндров (мебель, ящики, приборы, банки). Получится похоже.
- **🟡 можно, но грубее** — живая или мягкая форма (растения, еда, ткань, верёвка, костёр, машина). Будет заметно проще картинки.
- **❌ не сейчас** — нужен скелет (люди, животные, одежда на теле). Картинок для них в ОС и нет.

Нет картинки в ОС (43 объекта): все люди и существа, одежда на теле (`cloth_*`, `vest_armor`, `mask_gas`), `door_wood`, `door_metal`,
`car_wreck`, `dumpster`, `street_lamp`, `bench_street`, `watchtower`, `trade_stall`, `noticeboard`, `faction_banner`, `faction_stockpile`,
`scrap_pile`, `pyre_pile`, `grave_mound`, `blood_stain`, `battery_cell`, `fertilizer_bag`, `map_paper`, `mat_scrap`, `medical_kit`, `note_diary`,
`seed_bag`, `water_tablets`, `tool_flashlight`, `tool_knife`, `tool_soldering`, `weapon_bow`. Простые из них (двери, мусорный бак, скамейка, фонарь)
можно делать и без картинки — по описанию.

Не взяты: `block_*` (это текстуры земли и камня для тайлов, а не предметы), `billboard_road` и `treadmill_generator` (нет в списке объектов).

## Мебель (`furniture`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `bathtub` | Ванна | 170 × 60 | [chugunnaya](ref/furniture/bathtub.png) | ✅ | emalirovannaya, plastikovaya |
| `bed_single` | Кровать | 200 × 60 | [zheleznaya_koyka](ref/furniture/bed_single.png) | ✅ | derevyannaya_samodelnaya, isporchennaya_slomannaya, krovat_s_tumboy, nizkaya_matras_na_podstavke |
| `bunk_bed` | Двухъярусная койка | 200 × 180 | [derevyannaya](ref/furniture/bunk_bed.png) | ✅ | metallicheskaya |
| `chair_wood` | Стул | 45 × 90 | [derevyannyy](ref/furniture/chair_wood.png) | ✅ | barnyy_stul, kreslo, myagkiy_stul, taburet |
| `cot_medical` | Медицинская койка | 190 × 80 | [bolnichnaya](ref/furniture/cot_medical.png) | ✅ | polevaya, skladnaya |
| `planter_box` | Грядка | 120 × 40 | [derevo_pustoe](ref/furniture/planter_box.png) | ✅ | derevyannyy_yaschik_grunt, derevyannyy_yaschik, gidroponnyy_lotok_grunt, gidroponnyy_lotok, kirpichnaya_gryadka_grunt… |
| `sink_tap` | Раковина с краном | 80 × 90 | [kuhonnaya](ref/furniture/sink_tap.png) | ✅ | ulichnaya_kolonka, umyvalnik, vannaya |
| `table_wood` | Стол | 120 × 75 | [obedennyy](ref/furniture/table_wood.png) | ✅ | kuhonnyy_stol, pismennyy, skladnoy |
| `toilet` | Унитаз | 40 × 75 | [fayansovyy_so_smyvom](ref/furniture/toilet.png) | ✅ | samodelnyy_vedro_s_sidenem, slomannyy_zabroshennyy, suhoy_kompostnyy |

## Хранилища (`container`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `barrel_water` | Бочка для воды | 60 × 90 | [bochka_metal_100_l](ref/container/barrel_water.png) | ✅ | 15_litrov, bochka_derevo_100_l, bochka_plastik_100l, bochka_plastik_50l |
| `battery_bank` | Аккумулятор | 60 × 40 | [avtomobilnyy_12_v](ref/container/battery_bank.png) | ✅ | bunkernaya_batareya_bolshaya, bvtareyka, krona, paverbank |
| `crate_wood` | Деревянный ящик | 60 × 50 | [voennyy](ref/container/crate_wood.png) | ✅ | bolshoy, malyy, otkrytyy_razgrablennyy, sredniy |
| `first_aid_kit` | Аптечка | 25 × 18 | [avtomobilnaya](ref/container/first_aid_kit.png) | ✅ | domashnyaya, medetsinskaya, neotlozhka, pustaya, voennaya_bogache |
| `fuel_canister` | Канистра с топливом | 35 × 45 | [10_l](ref/container/fuel_canister.png) | ✅ | 20_l_zherri, 5_l |
| `kitchen_counter` | Кухонная тумба | 120 × 90 | [s_yaschikami](ref/container/kitchen_counter.png) | ✅ | dlinnaya, komod_metal_yaschiki, komod_tri_yaschika, otkrytye_polki, rakovina, rakovina_kran, s_dveryami, s_konforkoy,… |
| `locker_metal` | Шкафчик металлический | 50 × 180 | [armeyskiy](ref/container/locker_metal.png) | ✅ | ofisnyy, sportivnyy |
| `medicine_cabinet` | Аптечный шкафчик | 50 × 60 | [medpunkt_steklyannyy](ref/container/medicine_cabinet.png) | ✅ | metallicheskiy, vannyy |
| `rack_metal` | Стеллаж металлический | 120 × 200 | [promyshlennyy](ref/container/rack_metal.png) | ✅ | s_3_polkami, s_5_polkami |
| `safe_metal` | Сейф | 50 × 60 | [napolnyy](ref/container/safe_metal.png) | ✅ | nastennyy, seyf_yacheyka |
| `shelf_wood` | Полка | 100 × 30 | [derevyannaya_prostaya](ref/container/shelf_wood.png) | ✅ | derevyannaya_kruglyy_krepezh, derevyannaya_metal_ugolok, derevyannaya_na_trosah, dvoynaya, metal_s_kryuchkami, metal_… |
| `tank_water` | Резервуар воды | 160 × 190 | [stalnoy_tsilindr](ref/container/tank_water.png) | ✅ | — |
| `toolbox` | Ящик с инструментами | 40 × 25 | [krutoy](ref/container/toolbox.png) | ✅ | metallicheskiy, plastikovyy |
| `wardrobe` | Шкаф | 100 × 200 | [metallicheskiy_shkafchik](ref/container/wardrobe.png) | ✅ | derevyannyy_dvustvorchatyy_otkryt, derevyannyy_dvustvorchatyy_zakryt, garderob_s_zerkalom |

## Верстаки (`workbench`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `recycler_bench` | Стол разборки | 130 × 95 | [ruchnoy_derevyannyy](ref/workbench/recycler_bench.png) | ✅ | ruchnoy_metallicheskiy |
| `sewing_table` | Швейный стол | 110 × 85 | [pedalnaya](ref/workbench/sewing_table.png) | 🟡 | ruchnaya_mashina |
| `workbench_basic` | Верстак | 160 × 95 | [derevyannyy_bazovyy](ref/workbench/workbench_basic.png) | ✅ | metallicheskiy_s_tiskami, metallicheskiy_tyazhelyy, skladnoy_pohodnyy |
| `workbench_electronics` | Электронный верстак | 140 × 95 | [nastolnyy_pegboard](ref/workbench/workbench_electronics.png) | ✅ | nastolnyy_s_yaschikami |

## Машины и приборы (`machine`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `bike_generator` | Велогенератор | 120 × 110 | [skladnoy](ref/machine/bike_generator.png) | ✅ | statsionarnyy |
| `campfire` | Костёр | 80 × 50 | [koster_s_kotlom](ref/machine/campfire.png) | 🟡 | prostoy, s_kamnyami |
| `car_abandoned` | Брошенная машина | 450 × 160 | [sedan](ref/machine/car_abandoned.png) | 🟡 | gruzovik, mikroavtobus, perevernutaya, sgorevshaya |
| `fridge` | Холодильник | 70 × 180 | [elektricheskiy](ref/machine/fridge.png) | ✅ | morozilnaya_kamera, yaschik_so_ldom |
| `fuel_generator` | Генератор на топливе | 70 × 60 | [portativnyy](ref/machine/fuel_generator.png) | ✅ | promyshlennyy, statsionarnyy |
| `fuse_box` | Электрощит | 40 × 50 | [samodelnyy](ref/machine/fuse_box.png) | ✅ | — |
| `grow_lamp` | Лампа для урожая | 80 × 15 | [fioletovaya_led](ref/machine/grow_lamp.png) | ✅ | lyuminestsentnaya, slabaya |
| `hydro_rack` | Гидропонная стойка | 100 × 180 | [bolshaya](ref/machine/hydro_rack.png) | 🟡 | derevyannaya_grunt, derevyannaya_rostenie, malaya, plastik_grunt, plastik_rostenie |
| `lamp_ceiling` | Лампа потолочная | 30 × 25 | [nakalivaniya_plafon_zelenyy_amfora](ref/machine/lamp_ceiling.png) | ✅ | **Модель сделана как `lyuminestsentnaya` (с листа автора) — завести вариант в ОС.** krasnaya_klaksa, lyustra_zelenaya, nakalivaniya_plafon_bahroma |
| `light_switch` | Выключатель | 8 × 12 | [klavishnyy](ref/machine/light_switch.png) | ✅ | rychazhnyy_promyshlennyy, tumbler_na_schitke |
| `radio_desk` | Радиоприёмник | 35 × 25 | [voennaya_ratsiya](ref/machine/radio_desk.png) | ✅ | fm_boombox, fm_vintage, nastolnyy_lampovyy, nastolnyy_standart, ruchnoy_s_dinamo |
| `rain_collector` | Дождеуловитель | 110 × 60 | [bolshaya_ploschadka_dlya_bashni](ref/machine/rain_collector.png) | ✅ | kryshnaya_voronka, plenka_i_zhelob |
| `shelter_panel` | Панель убежища | 60 × 70 | [ekran_s_grafikami_pozzhe](ref/machine/shelter_panel.png) | ✅ | prostoy_pult |
| `solar_panel` | Солнечная панель | 120 × 80 | [bolshaya_300_vt](ref/machine/solar_panel.png) | ✅ | malaya_100_vt, skladnaya_portativnaya |
| `stove_cook` | Плита | 70 × 90 | [drovyanaya](ref/machine/stove_cook.png) | ✅ | elektricheskaya, gazovaya |
| `stove_heat` | Печь-буржуйка | 60 × 90 | [stalnaya_bochka](ref/machine/stove_heat.png) | ✅ | kirpichnaya, pohodnaya |
| `water_pump` | Насос | 50 × 60 | [benzinovyy](ref/machine/water_pump.png) | ✅ | elektricheskiy, ruchnoy_rychazhnyy |
| `water_purifier` | Очиститель воды | 60 × 100 | [himicheskie_tabletki_rashodnik](ref/machine/water_purifier.png) | ✅ | keramicheskiy_filtr, slabyy_filtr, ugolnyy_filtr |
| `wind_turbine` | Ветрогенератор | 100 × 300 | [malyy_gorizontalnyy](ref/machine/wind_turbine.png) | 🟡 | samodelnyy_iz_ventilyatora, vertikalnyy |

## Двери и указатели (`door`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `hatch_bunker` | Люк бункера | 100 × 60 | [lyuk_s_kolesom_zakrytyy](ref/door/hatch_bunker.png) | ✅ | lyuk_bunkekra_otkrytyy, lyuk_bunkekra_zakrytyy, lyuk_s_kolesom_otkrytyy, shlyuz_dvoynoy_otkryty, shlyuz_dvoynoy_zakrytyy |
| `signpost_fork` | Указатель развилки | 80 × 220 | [derevyannyy_s_verevkoy](ref/door/signpost_fork.png) | ✅ | dorozhnyy_znak, metallicheskiy_tsvetnoy, rzhavyy_chastichno_chitaetsya, samodelnyy_ukazatel, staryy_zhelescheyy_ukazatel |

## Строительное (`building`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `barricade_planks` | Баррикада | 110 × 200 | [doski_na_okne](ref/building/barricade_planks.png) | ✅ | mebel_u_dveri |
| `fence_wire` | Забор с колючей проволокой | 200 × 150 | [setka](ref/building/fence_wire.png) | ✅ | derevyannyy_chastokol |
| `ladder_metal` | Металлическая лестница | 50 × 300 | [verevochnaya](ref/building/ladder_metal.png) | ✅ | — |
| `stairs_wood` | Лестница | 110 × 260 | [derevyannaya](ref/building/stairs_wood.png) | ✅ | metallicheskaya |
| `tent_camp` | Палатка | 220 × 140 | [kupol_zelenaya](ref/building/tent_camp.png) | 🟡 | belaya_s_pechkoy, bolshaya_mnogokomnatnaya, kamuflyazh, klin_s_fonarem, kupol_s_ryukzakom, kupol_sinyaya, naves_otkrytyy |
| `water_tower` | Водонапорная башня | 400 × 1000 | [kirpichnaya](ref/building/water_tower.png) | ✅ | reshetchataya, stalnaya_bak |
| `window_basic` | Окно | 100 × 100 | [zakolochennoe](ref/building/window_basic.png) | ✅ | razbitoe, reshetka, tseloe |

## Декор (`decor`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `clock_wall` | Часы настенные | 30 × 30 | [elektronika_retro_alt](ref/decor/clock_wall.png) | ✅ | kvarts_metal_alt, metal_analog, smart_round_alt, wood_analog |

## Ресурсы (`resource`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `well_hand` | Колодец / скважина | 90 × 130 | [ruchnoy_kolodets_s_vorotom](ref/resource/well_hand.png) | 🟡 | skvazhina_s_elektronasosom, skvazhina_s_ruchnoy_pompoy |

## Инструменты (`tool`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `bucket` | Ведро | 30 × 30 | [kozhenoe_samodelnoe](ref/tool/bucket.png) | 🟡 | metallicheskoe, plastikovoe |
| `cooking_pot` | Кастрюля / котелок | 25 × 20 | [chugunnyy](ref/tool/cooking_pot.png) | ✅ | kotelok |
| `tool_axe` | Топор | 35 × 60 | [kamennyy_samodelnyy_icon](ref/tool/tool_axe.png) | ✅ | — |
| `tool_can_opener` | Консервный нож | 15 × 8 | [klyuch_otkryvashka_icon](ref/tool/tool_can_opener.png) | ✅ | — |
| `tool_crowbar` | Лом | 70 × 8 | [gvozdoder](ref/tool/tool_crowbar.png) | ✅ | — |
| `tool_hammer` | Молоток | 30 × 10 | [kuvaldochka_icon](ref/tool/tool_hammer.png) | ✅ | — |
| `tool_lockpick` | Отмычки | 10 × 5 | [nabor](ref/tool/tool_lockpick.png) | ✅ | samodelnye |
| `tool_pickaxe` | Кирка | 35 × 60 | [otboynyy_molotok_energiya_ikonka](ref/tool/tool_pickaxe.png) | ✅ | samodelnaya_idel |
| `tool_saw` | Пила | 50 × 12 | [benzopila_redkaya_shumnaya](ref/tool/tool_saw.png) | 🟡 | — |
| `tool_screwdriver` | Отвёртка | 20 × 4 | [nabor](ref/tool/tool_screwdriver.png) | ✅ | — |
| `tool_shovel` | Лопата | 30 × 110 | [sapernaya_skladnaya](ref/tool/tool_shovel.png) | ✅ | — |
| `tool_sledge` | Кувалда | 30 × 90 | [malaya](ref/tool/tool_sledge.png) | ✅ | molot_kirka |
| `tool_wrench` | Гаечный ключ | 30 × 8 | [nabor_klyuchey](ref/tool/tool_wrench.png) | ✅ | — |

## Оружие (`weapon`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `trap_bear` | Капкан / ловушка | 40 × 10 | [kapkan](ref/weapon/trap_bear.png) | 🟡 | petlya, yama_s_kolyami |
| `weapon_bat` | Бейсбольная бита | 90 × 10 | [derevyannaya](ref/weapon/weapon_bat.png) | ✅ | s_gvozdyami |
| `weapon_machete` | Мачете | 70 × 8 | [nozh_kukri](ref/weapon/weapon_machete.png) | ✅ | topor_machete |
| `weapon_pipe` | Труба-дубинка | 80 × 8 | [s_shipami](ref/weapon/weapon_pipe.png) | ✅ | stalnaya_truba |
| `weapon_pistol` | Пистолет | 20 × 14 | [9_mm](ref/weapon/weapon_pistol.png) | ✅ | revolver, samodelnyy |
| `weapon_shotgun` | Дробовик | 100 × 15 | [dvustvolka](ref/weapon/weapon_shotgun.png) | ✅ | obrez, pompovyy |

## Предметы (`item`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `ammo_9mm` | Патроны 9 мм | 6 × 3 | [broneboynye](ref/item/ammo_9mm.png) | ✅ | obychnye, samodelnye |
| `ammo_shells` | Патроны для дробовика | 8 × 4 | [kartech](ref/item/ammo_shells.png) | ✅ | pulya |
| `antibiotics` | Антибиотики | 6 × 8 | [broad_spectrum](ref/item/antibiotics.png) | ✅ | expired, narrow_spectrum |
| `antiseptic` | Антисептик | 6 × 14 | [perekis](ref/item/antiseptic.png) | ✅ | spirt, yod |
| `bandage` | Бинт | 10 × 6 | [elastichnyy](ref/item/bandage.png) | ✅ | ispolzovannyy, samodelnyy_iz_tkani, sterilnyy |
| `bottle_water` | Бутылка с водой | 8 × 25 | [flyaga_icon](ref/item/bottle_water.png) | ✅ | — |
| `coal_chunk` | Уголь | 15 × 12 | [kamennyy](ref/item/coal_chunk.png) | 🟡 | — |
| `duct_tape` | Изолента / скотч | 10 × 10 | [izolenta](ref/item/duct_tape.png) | ✅ | serebristaya_lenta, skotch |
| `food_bread` | Хлеб / сухари | 20 × 10 | [hleb](ref/item/food_bread.png) | 🟡 | lepeshka, suhari_dolgo |
| `food_canned` | Консервы | 8 × 10 | [tushenka_svinaya](ref/item/food_canned.png) | ✅ | ananas, baked_beans, beef_stew, boby, chechevittsa, condensed_milk, fasol, goroshek, grechka, green_peas, griby, kash… |
| `food_grain` | Зерно | 15 × 15 | [kukuruza_bochka](ref/item/food_grain.png) | ✅ | kukuruza_meshok, pshenitsa, ris |
| `fuel_firewood` | Дрова | 40 × 15 | [doskm](ref/item/fuel_firewood.png) | ✅ | otsyrevshie_goryat_huzhe, polenya, vyazanka_hvorosta |
| `iron_ore` | Железная руда | 15 × 12 | [oblomki_rudy](ref/item/iron_ore.png) | 🟡 | ruda |
| `key_generic` | Ключ | 3 × 8 | [brelok_s_nomerom](ref/item/key_generic.png) | ✅ | klyuch_karta, obychnyy |
| `lightbulb` | Лампочка | 6 × 12 | [lyuminestsentnaya_trubka_teplaya](ref/item/lightbulb.png) | ✅ | nakalivaniya_patron_golaya_lampa, nakalivaniya_prostaya, visit |
| `lock_padlock` | Навесной замок | 6 × 10 | [kodovyy](ref/item/lock_padlock.png) | ✅ | navesnoy, vreznoy |
| `mat_cement` | Цемент / стройматериалы | 30 × 40 | [gotovye_bloki](ref/item/mat_cement.png) | ✅ | meshok_tsementa |
| `mat_cloth` | Ткань | 30 × 20 | [loskut_2](ref/item/mat_cloth.png) | 🟡 | — |
| `mat_glass` | Стекло | 30 × 30 | [butylochnoe_steklo](ref/item/mat_glass.png) | 🟡 | list_stekla, oskolki |
| `mat_log` | Брёвна | 120 × 20 | [drova](ref/item/mat_log.png) | ✅ | poleno |
| `mat_nails` | Гвозди / крепёж | 6 × 4 | [gvozdi](ref/item/mat_nails.png) | ✅ | shurupy, skoby |
| `mat_pipe_metal` | Труба | 100 × 8 | [mednaya_2](ref/item/mat_pipe_metal.png) | ✅ | — |
| `mat_plank` | Доски | 100 × 10 | [brus_2](ref/item/mat_plank.png) | ✅ | — |
| `mat_rope` | Верёвка | 30 × 10 | [neylon](ref/item/mat_rope.png) | 🟡 | tros |
| `mat_rubble` | Строительный мусор | 20 × 15 | [betonnaya_kroshka](ref/item/mat_rubble.png) | 🟡 | bityy_kirpich |
| `mat_sheet_metal` | Металлический лист | 100 × 3 | [otsinkovannyy_2](ref/item/mat_sheet_metal.png) | ✅ | — |
| `mat_wire` | Проволока / провод | 20 × 20 | [mednaya_2](ref/item/mat_wire.png) | 🟡 | — |
| `meal_soup` | Готовое блюдо (суп, рагу) | 15 × 10 | [kasha_icon](ref/item/meal_soup.png) | 🟡 | — |
| `meat_cooked` | Приготовленное мясо | 15 × 8 | [kopchenoe_dolgo_hranitsya](ref/item/meat_cooked.png) | 🟡 | zharenoe_kuritsa_golen, zharenoe_kuritsa_grudka, zharenoe_kuritsa_tselaya, zharenoe_nadkusannoe, zharenoe_narezka, zh… |
| `meat_raw` | Сырое мясо | 15 × 8 | [myaso_beykon](ref/item/meat_raw.png) | 🟡 | myaso_nadkusannoe, myaso_narezka, myaso_rebra, myaso_steyk, ptitsa_golen, ptitsa_grudka, ptitsa_tselaya |
| `painkiller` | Обезболивающее | 6 × 8 | [analgin](ref/item/painkiller.png) | ✅ | aspirin, diclofenac, ibuprofen, ketorolac, morphine, paracetamol, tramadol |
| `part_electronic` | Электронные компоненты | 10 × 10 | [akkumulyatornye_elementy_2](ref/item/part_electronic.png) | ✅ | — |
| `part_mech` | Механические детали | 15 × 15 | [podshipniki_2](ref/item/part_mech.png) | ✅ | — |
| `part_rare_circuit` | Редкая схема | 10 × 10 | [voennaya_plata_2](ref/item/part_rare_circuit.png) | ✅ | — |
| `poison_vial` | Яд | 5 × 10 | [antidot_obratnoe](ref/item/poison_vial.png) | ✅ | medlennyy, silnyy, slabyy |
| `power_cable` | Провод / кабель | 20 × 20 | [silovoy](ref/item/power_cable.png) | 🟡 | — |
| `ration_dry` | Сухпаёк | 15 × 10 | [armeyskiy](ref/item/ration_dry.png) | ✅ | kosmicheskiy_redkiy, spasatelnyy_nabor |
| `repair_kit` | Ремонтный набор | 25 × 15 | [elektronnyy_remontnyy_nabor](ref/item/repair_kit.png) | ✅ | nabor_mehanika |
| `soap` | Мыло | 8 × 4 | [dezinfitsiruyuschee](ref/item/soap.png) | ✅ | gel, kusok_myla |
| `soil_clump` | Грунт | 15 × 12 | [chernozem](ref/item/soil_clump.png) | 🟡 | glina, pesok |
| `splint` | Шина | 40 × 8 | [gotovaya_icon](ref/item/splint.png) | 🟡 | — |
| `stone_chunk` | Кусок камня | 15 × 12 | [bulyzhnik_2](ref/item/stone_chunk.png) | 🟡 | — |
| `veg_potato` | Овощи (картофель, морковь) | 8 × 8 | [kukuruza](ref/item/veg_potato.png) | 🟡 | luk, morkov, pomidor |

## Растения (`plant`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `bush_berry` | Ягодный куст | 80 × 70 | [chernika](ref/plant/bush_berry.png) | 🟡 | malina, snotvornye_yagody, yadovitye_yagody |
| `plant_potato` | Картофель (растение) | 40 × 40 | [kartofel_growing](ref/plant/plant_potato.png) | 🟡 | kartofel, kukuruza_growing, kukuruza, morkov_growing, morkov, pomidor_growing, pomidor |
| `plant_tree` | Дерево | 160 × 450 | [sosna](ref/plant/plant_tree.png) | 🟡 | bereza, boto, buk, dub, el, iva, molodoe, opasnoe, opasnoe_povalenoe, pen_gribnyy, pen, povalenoe, suhoe_derevo |
| `plant_wheat` | Пшеница (растение) | 50 × 80 | [pshenitsa](ref/plant/plant_wheat.png) | 🟡 | rozh |

## Одежда (`clothing`)

| id | Название | Ш × В, см | Картинка | Сложность | Ещё в ОС |
|---|---|---|---|---|---|
| `backpack` | Рюкзак | 35 × 45 | [shkolnyy_malyy](ref/clothing/backpack.png) | 🟡 (рюкзак — на спину, как отдельная вещь) | sumka_cherez_plecho, turisticheskiy, voennyy_bolshoy |
