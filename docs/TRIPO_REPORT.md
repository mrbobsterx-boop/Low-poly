# Отчёт обработки моделей из Tripo

Делает `tools/tripo_process.py` (правила — `docs/TRIPO.md`, раздел 2). Данные — `docs/tripo_report.json`.

| Модель (export/) | Файл из tripo/ | Треугольники до → после (лимит) | Размер Ш × Г × В, см | ОС Ш × В, см | Масштаб | Поворот | Крепление | Текстуры | Файл, МБ | Предупреждения |
|---|---|---|---|---|---|---|---|---|---|---|
| `ammo_9mm_obychnye_idle` | `ammo_9mm_obychnye.glb` | 47 534 → 2 940 (3 000) | 6 × 5 × 8 | 6 × 3 | ×0.0823 | 270° | floor | 1 шт. 2048→512 | 0.16 | ⚠ подогнано по ширине; высота 8 см  в ОС 3 см |
| `ammo_shells_kartech_idle` | `ammo_shells_kartech.glb` | 48 750 → 2 940 (3 000) | 8 × 7 × 5 | 8 × 4 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.16 | — |
| `antibiotics_shirokogo_spektra_idle` | `antibiotics_shirokogo_spektra.glb` | 46 530 → 2 940 (3 000) | 8 × 3 × 2 | 6 × 8 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.13 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (8 см); высота 2 см  в ОС 8 см |
| `antiseptic_spirt_idle` | `antiseptic_spirt.glb` | 46 206 → 2 940 (3 000) | 8 × 7 × 14 | 6 × 14 | ×0.14 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ ширина 8 см  в ОС 6 см (> 15 %) — записано в DEVIATIONS.md |
| `apartments_b_idle` | `apartments_b.glb` | 39 753 → 14 699 (15 000) | 1400 × 859 × 801 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 1.03 | ⚠ подогнано по ширине; высота 801 см  в ОС 600 см |
| `apartments_c_idle` | `apartments_c.glb` | 42 570 → 14 700 (15 000) | 1200 × 646 × 1341 | 1200 × 600 | ×13.4 | 270° | floor | 1 шт. 2048→1024 | 1.10 | ⚠ подогнано по ширине; высота 1341 см  в ОС 600 см |
| `apartments_idle` | `apartments.glb` | 42 427 → 14 700 (15 000) | 1200 × 621 × 1477 | 1200 × 600 | ×14.8 | 270° | floor | 1 шт. 2048→1024 | 1.07 | ⚠ подогнано по ширине; высота 1477 см  в ОС 600 см |
| `auto_repair_idle` | `auto_repair.glb` | 38 566 → 14 700 (15 000) | 1000 × 902 × 579 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.81 | — |
| `awning_striped_b_idle` | `awning_striped_b.glb` | 44 368 → 14 700 (15 000) | 279 × 153 × 250 | 100 × 250 | ×2.79 | 270° | floor | 1 шт. 2048→1024 | 0.49 | — |
| `awning_striped_idle` | `awning_striped.glb` | 42 576 → 14 700 (15 000) | 280 × 131 × 250 | 100 × 250 | ×2.8 | 270° | floor | 1 шт. 2048→1024 | 0.50 | — |
| `backpack_shkolnyy_idle` | `backpack_shkolnyy.glb` | 47 870 → 2 940 (3 000) | 38 × 36 × 45 | 35 × 45 | ×0.45 | 270° | floor | 1 шт. 2048→512 | 0.18 | — |
| `bandage_sterilnyy_idle` | `bandage_sterilnyy.glb` | 49 664 → 2 940 (3 000) | 10 × 12 × 11 | 10 × 6 | ×0.116 | 270° | floor | 1 шт. 2048→512 | 0.19 | ⚠ подогнано по ширине; высота 11 см  в ОС 6 см |
| `barrel_water_plastikovaya_200_l_idle` | `barrel_water_plastikovaya_200_l.glb` | 48 658 → 7 840 (8 000) | 51 × 63 × 90 | 60 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.32 | — |
| `barricade_planks_doski_na_okne_idle` | `barricade_planks_doski_na_okne.glb` | 47 702 → 14 698 (15 000) | 163 × 68 × 200 | 110 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.55 | ⚠ ширина 163 см  в ОС 110 см (> 15 %) — записано в DEVIATIONS.md |
| `bathtub_chugunnaya_idle` | `bathtub_chugunnaya.glb` | 48 116 → 7 840 (8 000) | 170 × 124 × 107 | 170 × 60 | ×1.7 | 0° | floor | 1 шт. 2048→1024 | 0.28 | ⚠ подогнано по ширине; высота 107 см  в ОС 60 см |
| `battery_bank_avtomobilnyy_12_v_idle` | `battery_bank_avtomobilnyy_12_v.glb` | 43 149 → 7 839 (8 000) | 36 × 38 × 40 | 60 × 40 | ×0.4 | 270° | floor | 1 шт. 2048→1024 | 0.31 | ⚠ ширина 36 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `battery_cell_odnorazovaya_idle` | `battery_cell_odnorazovaya.glb` | 48 078 → 2 940 (3 000) | 2 × 2 × 6 | 3 × 6 | ×0.06 | 270° | floor | 1 шт. 2048→512 | 0.12 | ⚠ ширина 2 см  в ОС 3 см (> 15 %) — записано в DEVIATIONS.md |
| `bed_single_zheleznaya_koyka_idle` | `bed_single_zheleznaya_koyka.glb` | 44 886 → 7 840 (8 000) | 200 × 108 × 80 | 200 × 60 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.37 | ⚠ подогнано по ширине; высота 80 см  в ОС 60 см |
| `bench_street_derevyannaya_idle` | `bench_street_derevyannaya.glb` | 45 972 → 7 840 (8 000) | 150 × 97 × 92 | 150 × 80 | ×1.5 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `bicycle_idle` | `bicycle.glb` | 48 518 → 7 840 (8 000) | 180 × 60 × 107 | 180 × 150 | ×1.8 | 0° | floor | 1 шт. 2048→1024 | 0.53 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (180 см); высота 107 см  в ОС 150 см |
| `bike_generator_statsionarnyy_idle` | `bike_generator_statsionarnyy.glb` | 45 800 → 14 700 (15 000) | 120 × 71 × 110 | 120 × 110 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.63 | — |
| `billboard_road_tselyy_idle` | `billboard_road_tselyy.glb` | 46 144 → 14 700 (15 000) | 231 × 79 × 400 | 150 × 400 | ×4 | 270° | floor | 1 шт. 2048→1024 | 0.55 | ⚠ ширина 231 см  в ОС 150 см (> 15 %) — записано в DEVIATIONS.md |
| `block_bedrock_idle` | `block_bedrock.glb` | 49 636 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.04 | 0° | floor | 1 шт. 2048→1024 | 0.32 | — |
| `block_brick_idle` | `block_brick.glb` | 39 451 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.74 | — |
| `block_clay_idle` | `block_clay.glb` | 48 676 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.01 | 0° | floor | 1 шт. 2048→1024 | 0.27 | — |
| `block_concrete_cracked_idle` | `block_concrete_cracked.glb` | 47 163 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.01 | 0° | floor | 1 шт. 2048→1024 | 0.53 | — |
| `block_concrete_idle` | `block_concrete.glb` | 47 940 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.40 | — |
| `block_dirt_cracked_idle` | `block_dirt_cracked.glb` | 48 891 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.19 | 270° | floor | 1 шт. 2048→1024 | 0.47 | — |
| `block_dirt_idle` | `block_dirt.glb` | 46 923 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.04 | 0° | floor | 1 шт. 2048→1024 | 0.61 | — |
| `block_grass_idle` | `block_grass.glb` | 44 881 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.07 | 0° | floor | 1 шт. 2048→1024 | 0.43 | — |
| `block_gravel_idle` | `block_gravel.glb` | 47 145 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.01 | 0° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `block_metal_idle` | `block_metal.glb` | 48 056 → 7 838 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.04 | 0° | floor | 1 шт. 2048→1024 | 0.42 | — |
| `block_sand_idle` | `block_sand.glb` | 48 129 → 7 839 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.02 | 0° | floor | 1 шт. 2048→1024 | 0.30 | — |
| `block_soil_layers_b_idle` | `block_soil_layers_b.glb` | 48 602 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.38 | — |
| `block_soil_layers_idle` | `block_soil_layers.glb` | 48 602 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.38 | — |
| `block_stone_idle` | `block_stone.glb` | 47 772 → 7 840 (8 000) | 100 × 100 × 100 | 100 × 100 | ×1.06 | 0° | floor | 1 шт. 2048→1024 | 0.27 | — |
| `body_base_female_idle` | `body_base_female.glb` | 47 294 → 14 700 (15 000) | 163 × 34 × 170 | 170 × 170 | ×1.7 | 0° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ в файле 2 отдельных объектов — склеены в один |
| `bottle_water_plastikovaya_0_5_l_idle` | `bottle_water_plastikovaya_0_5_l.glb` | 48 176 → 2 940 (3 000) | 10 × 10 × 25 | 8 × 25 | ×0.25 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ ширина 10 см  в ОС 8 см (> 15 %) — записано в DEVIATIONS.md |
| `bucket_metallicheskoe_idle` | `bucket_metallicheskoe.glb` | 47 746 → 2 940 (3 000) | 23 × 20 × 30 | 30 × 30 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.15 | ⚠ ширина 23 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `building_ruin_1_idle` | `building_ruin_1.glb` | 38 296 → 14 700 (15 000) | 1200 × 733 × 688 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.95 | — |
| `building_ruin_2_idle` | `building_ruin_2.glb` | 42 411 → 14 699 (15 000) | 1400 × 778 × 769 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.98 | ⚠ подогнано по ширине; высота 769 см  в ОС 600 см |
| `bunk_bed_metallicheskaya_idle` | `bunk_bed_metallicheskaya.glb` | 41 609 → 14 699 (15 000) | 200 × 125 × 149 | 200 × 180 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.58 | — |
| `bunting_b_idle` | `bunting_b.glb` | 47 762 → 7 840 (8 000) | 101 × 13 × 60 | 100 × 60 | ×1.01 | 270° | floor | 1 шт. 2048→1024 | 0.37 | — |
| `bunting_idle` | `bunting.glb` | 47 280 → 7 840 (8 000) | 92 × 8 × 60 | 100 × 60 | ×0.918 | 270° | floor | 1 шт. 2048→1024 | 0.40 | — |
| `bus_school_idle` | `bus_school.glb` | 43 466 → 7 840 (8 000) | 1100 × 372 × 380 | 1100 × 150 | ×11 | 90° | floor | 1 шт. 2048→1024 | 0.55 | ⚠ подогнано по ширине; высота 380 см  в ОС 150 см |
| `bush_berry_malina_idle` | `bush_berry_malina.glb` | 48 630 → 7 840 (8 000) | 57 × 39 × 70 | 80 × 70 | ×0.7 | 270° | floor | 1 шт. 2048→1024 | 0.60 | ⚠ ширина 57 см  в ОС 80 см (> 15 %) — записано в DEVIATIONS.md |
| `campfire_prostoy_idle` | `campfire_prostoy.glb` | 49 521 → 7 840 (8 000) | 118 × 117 × 50 | 80 × 50 | ×1.18 | 270° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ 5 отдельн. крупн. кус(ка/ков) в стороне от главного — возможно  лишняя вещь с картинки (рюкзак  ящик…) — посмотреть на превью<br>⚠ ширина 118 см  в ОС 80 см (> 15 %) — записано в DEVIATIONS.md |
| `car_abandoned_sedan_idle` | `car_abandoned_sedan.glb` | 46 098 → 14 700 (15 000) | 450 × 184 × 147 | 450 × 160 | ×4.5 | 270° | floor | 1 шт. 2048→1024 | 0.68 | — |
| `car_hatchback_idle` | `car_hatchback.glb` | 46 054 → 7 840 (8 000) | 400 × 212 × 166 | 400 × 150 | ×4 | 0° | floor | 1 шт. 2048→1024 | 0.47 | — |
| `car_old_blue_idle` | `car_old_blue.glb` | 46 367 → 7 839 (8 000) | 470 × 211 × 153 | 470 × 150 | ×4.7 | 90° | floor | 1 шт. 2048→1024 | 0.49 | — |
| `car_police_b_idle` | `car_police_b.glb` | 47 216 → 7 840 (8 000) | 480 × 201 × 147 | 480 × 150 | ×4.8 | 0° | floor | 1 шт. 2048→1024 | 0.46 | — |
| `car_police_idle` | `car_police.glb` | 47 404 → 7 840 (8 000) | 480 × 215 × 166 | 480 × 150 | ×4.8 | 0° | floor | 1 шт. 2048→1024 | 0.46 | — |
| `car_sedan_b_idle` | `car_sedan_b.glb` | 46 916 → 7 838 (8 000) | 450 × 190 × 155 | 450 × 150 | ×4.5 | 90° | floor | 1 шт. 2048→1024 | 0.48 | — |
| `car_sedan_idle` | `car_sedan.glb` | 45 928 → 7 840 (8 000) | 450 × 174 × 156 | 450 × 150 | ×4.5 | 0° | floor | 1 шт. 2048→1024 | 0.53 | — |
| `car_station_wagon_b_idle` | `car_station_wagon_b.glb` | 44 906 → 7 840 (8 000) | 480 × 200 × 166 | 480 × 150 | ×4.8 | 270° | floor | 1 шт. 2048→1024 | 0.48 | — |
| `car_station_wagon_idle` | `car_station_wagon.glb` | 44 665 → 7 839 (8 000) | 480 × 203 × 171 | 480 × 150 | ×4.8 | 270° | floor | 1 шт. 2048→1024 | 0.46 | — |
| `car_tarp_b_idle` | `car_tarp_b.glb` | 47 374 → 7 840 (8 000) | 450 × 197 × 147 | 450 × 150 | ×4.5 | 0° | floor | 1 шт. 2048→1024 | 0.41 | — |
| `car_tarp_idle` | `car_tarp.glb` | 46 872 → 7 840 (8 000) | 450 × 244 × 155 | 450 × 150 | ×4.5 | 90° | floor | 1 шт. 2048→1024 | 0.40 | — |
| `car_wreck_razobrannaya_idle` | `car_wreck_razobrannaya.glb` | 46 812 → 14 698 (15 000) | 450 × 176 × 127 | 450 × 150 | ×4.5 | 0° | floor | 1 шт. 2048→1024 | 0.61 | — |
| `chair_wood_derevyannyy_idle` | `chair_wood_derevyannyy.glb` | 42 230 → 7 838 (8 000) | 43 × 45 × 90 | 45 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.38 | — |
| `church_b_idle` | `church_b.glb` | 43 990 → 14 699 (15 000) | 1000 × 831 × 641 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 1.01 | — |
| `church_c_idle` | `church_c.glb` | 43 998 → 14 700 (15 000) | 1000 × 1449 × 1399 | 1000 × 600 | ×14.5 | 270° | floor | 1 шт. 2048→1024 | 0.93 | ⚠ подогнано по ширине; высота 1399 см  в ОС 600 см |
| `church_idle` | `church.glb` | 43 990 → 14 699 (15 000) | 1000 × 831 × 641 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 1.01 | — |
| `clinic_b_idle` | `clinic_b.glb` | 41 421 → 14 699 (15 000) | 1200 × 664 × 1058 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.97 | ⚠ подогнано по ширине; высота 1058 см  в ОС 600 см |
| `clinic_idle` | `clinic.glb` | 39 362 → 14 700 (15 000) | 1200 × 880 × 619 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.84 | — |
| `clock_wall_mehanicheskie_idle` | `clock_wall_mehanicheskie.glb` | 48 031 → 2 939 (3 000) | 30 × 6 × 30 | 30 × 30 | ×0.301 | 270° | wall | 1 шт. 2048→512 | 0.14 | — |
| `cloth_boots_krossovki_idle` | `cloth_boots_krossovki.glb` | 46 890 → 2 940 (3 000) | 30 × 21 × 9 | 30 × 20 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.20 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (30 см); высота 9 см  в ОС 20 см |
| `cloth_gloves_rabochie_idle` | `cloth_gloves_rabochie.glb` | 47 480 → 2 940 (3 000) | 20 × 17 × 5 | 20 × 15 | ×0.2 | 270° | floor | 1 шт. 2048→512 | 0.15 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (20 см); высота 5 см  в ОС 15 см |
| `cloth_jacket_kozhanaya_idle` | `cloth_jacket_kozhanaya.glb` | 48 026 → 7 838 (8 000) | 70 × 29 × 70 | 50 × 70 | ×0.7 | 270° | floor | 1 шт. 2048→1024 | 0.41 | ⚠ ширина 70 см  в ОС 50 см (> 15 %) — записано в DEVIATIONS.md |
| `cloth_pants_dzhinsy_idle` | `cloth_pants_dzhinsy.glb` | 47 834 → 7 840 (8 000) | 64 × 80 × 19 | 40 × 80 | ×0.8 | 270° | floor | 1 шт. 2048→1024 | 0.38 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (80 см); высота 19 см  в ОС 80 см |
| `coal_chunk_kamennyy_idle` | `coal_chunk_kamennyy.glb` | 47 212 → 2 940 (3 000) | 18 × 15 × 12 | 15 × 12 | ×0.182 | 270° | floor | 1 шт. 2048→512 | 0.13 | ⚠ ширина 18 см  в ОС 15 см (> 15 %) — записано в DEVIATIONS.md |
| `construction_site_idle` | `construction_site.glb` | 43 165 → 14 699 (15 000) | 1400 × 679 × 826 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.78 | ⚠ подогнано по ширине; высота 826 см  в ОС 600 см |
| `container_shack_idle` | `container_shack.glb` | 39 867 → 14 699 (15 000) | 600 × 383 × 399 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.79 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 399 см  в ОС 600 см |
| `cooking_pot_alyuminievaya_idle` | `cooking_pot_alyuminievaya.glb` | 48 104 → 2 940 (3 000) | 40 × 31 × 20 | 25 × 20 | ×0.399 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ ширина 40 см  в ОС 25 см (> 15 %) — записано в DEVIATIONS.md |
| `corpse_human_svezhee_idle` | `corpse_human_svezhee.glb` | 47 532 → 7 840 (8 000) | 180 × 127 × 44 | 180 × 30 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.51 | ⚠ подогнано по ширине; высота 44 см  в ОС 30 см |
| `corpse_zombie_svezhee_idle` | `corpse_zombie_svezhee.glb` | 49 086 → 7 840 (8 000) | 180 × 100 × 31 | 180 × 30 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.49 | — |
| `cot_medical_skladnaya_idle` | `cot_medical_skladnaya.glb` | 44 820 → 7 840 (8 000) | 190 × 100 × 77 | 190 × 80 | ×1.9 | 0° | floor | 1 шт. 2048→1024 | 0.36 | — |
| `crane_tower_idle` | `crane_tower.glb` | 43 010 → 14 700 (15 000) | 3337 × 651 × 2500 | 100 × 2500 | ×33.4 | 270° | floor | 1 шт. 2048→1024 | 0.79 | — |
| `crate_wood_malyy_idle` | `crate_wood_malyy.glb` | 40 005 → 7 839 (8 000) | 70 × 58 × 50 | 60 × 50 | ×0.703 | 270° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ ширина 70 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `crates_stack_idle` | `crates_stack.glb` | 45 231 → 14 699 (15 000) | 125 × 125 × 150 | 100 × 150 | ×1.5 | 0° | floor | 1 шт. 2048→1024 | 0.69 | — |
| `dam_idle` | `dam.glb` | 43 153 → 14 699 (15 000) | 2000 × 815 × 1314 | 2000 × 600 | ×20 | 90° | floor | 1 шт. 2048→1024 | 0.69 | ⚠ подогнано по ширине; высота 1314 см  в ОС 600 см |
| `decor_arch_wood_idle` | `decor_arch_wood.glb` | 38 325 → 14 699 (15 000) | 254 × 169 × 200 | 200 × 200 | ×2.54 | 270° | floor | 1 шт. 2048→1024 | 0.58 | ⚠ ширина 254 см  в ОС 200 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_armchair_idle` | `decor_armchair.glb` | 47 495 → 7 839 (8 000) | 103 × 87 × 95 | 90 × 95 | ×1.03 | 180° | floor | 1 шт. 2048→1024 | 0.27 | — |
| `decor_barrels_rusty_idle` | `decor_barrels_rusty.glb` | 47 826 → 7 840 (8 000) | 122 × 68 × 90 | 120 × 90 | ×1.22 | 270° | floor | 1 шт. 2048→1024 | 0.31 | ⚠ 1 отдельн. крупн. кус(ка/ков) в стороне от главного — возможно  лишняя вещь с картинки (рюкзак  ящик…) — посмотреть на превью |
| `decor_books_stack_idle` | `decor_books_stack.glb` | 45 966 → 2 940 (3 000) | 27 × 26 × 50 | 30 × 50 | ×0.5 | 270° | floor | 1 шт. 2048→512 | 0.21 | — |
| `decor_brick_wall_panel_idle` | `decor_brick_wall_panel.glb` | 40 965 → 14 700 (15 000) | 139 × 29 × 150 | 150 × 150 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.84 | — |
| `decor_cable_channel_idle` | `decor_cable_channel.glb` | 48 034 → 7 840 (8 000) | 100 × 20 × 8 | 100 × 10 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.34 | — |
| `decor_cart_crate_idle` | `decor_cart_crate.glb` | 40 971 → 7 840 (8 000) | 110 × 81 × 120 | 70 × 120 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.50 | ⚠ ширина 110 см  в ОС 70 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_chalkboard_easel_idle` | `decor_chalkboard_easel.glb` | 45 106 → 7 840 (8 000) | 96 × 54 × 110 | 70 × 110 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.40 | ⚠ ширина 96 см  в ОС 70 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_clothesline_idle` | `decor_clothesline.glb` | 49 012 → 7 840 (8 000) | 150 × 19 × 83 | 150 × 80 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.37 | — |
| `decor_column_rusty_idle` | `decor_column_rusty.glb` | 47 354 → 14 700 (15 000) | 47 × 82 × 300 | 40 × 300 | ×3 | 270° | floor | 1 шт. 2048→1024 | 0.43 | ⚠ ширина 47 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_container_panel_idle` | `decor_container_panel.glb` | 38 046 → 14 700 (15 000) | 190 × 146 × 200 | 100 × 200 | ×2 | 270° | wall | 1 шт. 2048→1024 | 0.56 | ⚠ ширина 190 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_cork_board_idle` | `decor_cork_board.glb` | 41 588 → 7 840 (8 000) | 79 × 5 × 70 | 90 × 70 | ×0.789 | 270° | wall | 1 шт. 2048→1024 | 0.40 | — |
| `decor_counter_wood_idle` | `decor_counter_wood.glb` | 44 110 → 7 840 (8 000) | 152 × 31 × 100 | 150 × 100 | ×1.52 | 270° | floor | 1 шт. 2048→1024 | 0.27 | — |
| `decor_curtain_idle` | `decor_curtain.glb` | 45 862 → 14 700 (15 000) | 167 × 31 × 200 | 120 × 200 | ×2 | 270° | wall | 1 шт. 2048→1024 | 0.51 | ⚠ ширина 167 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_door_frame_rusty_idle` | `decor_door_frame_rusty.glb` | 47 834 → 14 700 (15 000) | 98 × 56 × 210 | 100 × 210 | ×2.1 | 270° | floor | 1 шт. 2048→1024 | 0.42 | — |
| `decor_door_industrial_idle` | `decor_door_industrial.glb` | 43 651 → 14 699 (15 000) | 184 × 143 × 210 | 120 × 210 | ×2.1 | 270° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ ширина 184 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_electric_cabinet_idle` | `decor_electric_cabinet.glb` | 46 210 → 7 838 (8 000) | 66 × 59 × 140 | 60 × 140 | ×1.4 | 270° | floor | 1 шт. 2048→1024 | 0.35 | — |
| `decor_emblem_round_idle` | `decor_emblem_round.glb` | 47 024 → 7 840 (8 000) | 100 × 100 × 13 | 100 × 10 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.39 | ⚠ подогнано по ширине; высота 13 см  в ОС 10 см |
| `decor_extinguisher_1_idle` | `decor_extinguisher_1.glb` | 46 350 → 7 840 (8 000) | 23 × 18 × 60 | 25 × 60 | ×0.6 | 270° | wall | 1 шт. 2048→1024 | 0.31 | — |
| `decor_extinguisher_2_idle` | `decor_extinguisher_2.glb` | 46 420 → 7 838 (8 000) | 26 × 18 × 60 | 25 × 60 | ×0.6 | 270° | wall | 1 шт. 2048→1024 | 0.33 | — |
| `decor_foam_panels_idle` | `decor_foam_panels.glb` | 47 984 → 7 838 (8 000) | 100 × 15 × 60 | 100 × 60 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.41 | — |
| `decor_garland_lights_idle` | `decor_garland_lights.glb` | 47 971 → 7 839 (8 000) | 150 × 11 × 44 | 150 × 30 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.40 | ⚠ подогнано по ширине; высота 44 см  в ОС 30 см |
| `decor_gas_cylinders_idle` | `decor_gas_cylinders.glb` | 49 584 → 7 840 (8 000) | 55 × 45 × 140 | 50 × 140 | ×1.4 | 270° | floor | 1 шт. 2048→1024 | 0.37 | — |
| `decor_hose_hanging_idle` | `decor_hose_hanging.glb` | 48 464 → 7 838 (8 000) | 47 × 17 × 60 | 50 × 60 | ×0.6 | 0° | wall | 1 шт. 2048→1024 | 0.32 | — |
| `decor_junction_box_idle` | `decor_junction_box.glb` | 46 510 → 2 940 (3 000) | 75 × 56 × 30 | 40 × 30 | ×0.748 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ ширина 75 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_lamp_wall_industrial_idle` | `decor_lamp_wall_industrial.glb` | 47 310 → 2 940 (3 000) | 25 × 34 × 25 | 30 × 25 | ×0.341 | 270° | wall | 1 шт. 2048→512 | 0.20 | ⚠ ширина 25 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_light_panel_idle` | `decor_light_panel.glb` | 44 831 → 7 839 (8 000) | 120 × 12 × 26 | 120 × 15 | ×1.2 | 270° | ceiling | 1 шт. 2048→1024 | 0.33 | ⚠ подогнано по ширине; высота 26 см  в ОС 15 см |
| `decor_light_red_emergency_idle` | `decor_light_red_emergency.glb` | 47 234 → 2 940 (3 000) | 22 × 21 × 30 | 25 × 30 | ×0.3 | 270° | wall | 1 шт. 2048→512 | 0.16 | — |
| `decor_map_old_idle` | `decor_map_old.glb` | 47 250 → 7 838 (8 000) | 60 × 60 × 5 | 60 × 5 | ×0.602 | 0° | floor | 1 шт. 2048→1024 | 0.37 | — |
| `decor_metal_duct_idle` | `decor_metal_duct.glb` | 43 116 → 7 840 (8 000) | 150 × 49 × 44 | 150 × 30 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.32 | ⚠ подогнано по ширине; высота 44 см  в ОС 30 см |
| `decor_metal_wall_panel_idle` | `decor_metal_wall_panel.glb` | 44 563 → 7 839 (8 000) | 107 × 36 × 100 | 100 × 100 | ×1.07 | 270° | wall | 1 шт. 2048→1024 | 0.39 | — |
| `decor_pallet_idle` | `decor_pallet.glb` | 35 810 → 7 840 (8 000) | 120 × 120 × 16 | 120 × 15 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.34 | — |
| `decor_pipe_valves_idle` | `decor_pipe_valves.glb` | 44 034 → 14 700 (15 000) | 90 × 39 × 150 | 80 × 150 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.49 | — |
| `decor_pipes_colored_h_idle` | `decor_pipes_colored_h.glb` | 43 664 → 7 838 (8 000) | 150 × 22 × 40 | 150 × 20 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.38 | ⚠ подогнано по ширине; высота 40 см  в ОС 20 см |
| `decor_pipes_colored_v_idle` | `decor_pipes_colored_v.glb` | 49 256 → 14 698 (15 000) | 57 × 60 × 300 | 30 × 300 | ×3 | 270° | wall | 1 шт. 2048→1024 | 0.54 | ⚠ ширина 57 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_poster_mountain_idle` | `decor_poster_mountain.glb` | 46 194 → 7 840 (8 000) | 44 × 12 × 70 | 50 × 70 | ×0.7 | 270° | wall | 1 шт. 2048→1024 | 0.40 | — |
| `decor_rug_idle` | `decor_rug.glb` | 47 874 → 7 840 (8 000) | 200 × 166 × 9 | 200 × 5 | ×2 | 0° | floor | 1 шт. 2048→1024 | 0.53 | ⚠ подогнано по ширине; высота 9 см  в ОС 5 см |
| `decor_rug_round_idle` | `decor_rug_round.glb` | 46 952 → 7 840 (8 000) | 100 × 100 × 6 | 100 × 5 | ×1 | 0° | floor | 1 шт. 2048→1024 | 0.37 | — |
| `decor_sacks_idle` | `decor_sacks.glb` | 48 510 → 7 840 (8 000) | 100 × 87 × 58 | 100 × 60 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.38 | — |
| `decor_sign_exit_idle` | `decor_sign_exit.glb` | 47 650 → 2 940 (3 000) | 50 × 4 × 32 | 50 × 30 | ×0.5 | 270° | wall | 1 шт. 2048→512 | 0.15 | — |
| `decor_sign_warning_idle` | `decor_sign_warning.glb` | 47 680 → 7 840 (8 000) | 56 × 38 × 90 | 60 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `decor_steel_beam_idle` | `decor_steel_beam.glb` | 45 698 → 7 840 (8 000) | 150 × 36 × 25 | 150 × 15 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.33 | ⚠ подогнано по ширине; высота 25 см  в ОС 15 см |
| `decor_sticky_notes_wall_idle` | `decor_sticky_notes_wall.glb` | 46 665 → 7 839 (8 000) | 79 × 11 × 80 | 100 × 80 | ×0.8 | 270° | wall | 1 шт. 2048→1024 | 0.47 | ⚠ 50 отдельн. крупн. кус(ка/ков) в стороне от главного — возможно  лишняя вещь с картинки (рюкзак  ящик…) — посмотреть на превью<br>⚠ 48 кус(ка/ков) висит в воздухе<br>⚠ много мелких отдельных кусков (61) — Tripo мог «насорить»<br>⚠ ширина 79 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_street_lamp_post_idle` | `decor_street_lamp_post.glb` | 49 394 → 14 700 (15 000) | 111 × 41 × 400 | 40 × 400 | ×4 | 0° | floor | 1 шт. 2048→1024 | 0.43 | ⚠ ширина 111 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_tile_panel_white_idle` | `decor_tile_panel_white.glb` | 43 436 → 7 840 (8 000) | 120 × 22 × 100 | 100 × 100 | ×1.2 | 270° | wall | 1 шт. 2048→1024 | 0.33 | ⚠ ширина 120 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_tool_board_idle` | `decor_tool_board.glb` | 45 069 → 7 839 (8 000) | 102 × 11 × 80 | 120 × 80 | ×1.02 | 270° | wall | 1 шт. 2048→1024 | 0.58 | ⚠ ширина 102 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `decor_vault_door_round_idle` | `decor_vault_door_round.glb` | 46 990 → 14 698 (15 000) | 150 × 44 × 150 | 150 × 150 | ×1.5 | 270° | wall | 1 шт. 2048→1024 | 0.62 | — |
| `decor_vent_rusty_idle` | `decor_vent_rusty.glb` | 43 780 → 7 840 (8 000) | 60 × 10 × 60 | 60 × 60 | ×0.604 | 270° | wall | 1 шт. 2048→1024 | 0.34 | — |
| `decor_wood_molding_idle` | `decor_wood_molding.glb` | 44 116 → 7 840 (8 000) | 100 × 40 × 17 | 100 × 12 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.30 | ⚠ подогнано по ширине; высота 17 см  в ОС 12 см |
| `decor_wood_slat_panel_idle` | `decor_wood_slat_panel.glb` | 41 223 → 7 839 (8 000) | 117 × 58 × 100 | 100 × 100 | ×1.17 | 270° | wall | 1 шт. 2048→1024 | 0.41 | ⚠ ширина 117 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `diner_idle` | `diner.glb` | 39 285 → 14 699 (15 000) | 1000 × 1139 × 669 | 1000 × 600 | ×11.4 | 270° | floor | 1 шт. 2048→1024 | 1.04 | — |
| `dog_feral_odinochnaya_idle` | `dog_feral_odinochnaya.glb` | 49 506 → 14 700 (15 000) | 29 × 89 × 60 | 90 × 60 | ×0.885 | 270° | floor | 1 шт. 2048→1024 | 0.52 | ⚠ ширина 29 см  в ОС 90 см (> 15 %) — записано в DEVIATIONS.md |
| `donut_shop_idle` | `donut_shop.glb` | 46 767 → 14 699 (15 000) | 800 × 752 × 424 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.77 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (800 см); высота 424 см  в ОС 600 см |
| `door_metal_stalnaya_idle` | `door_metal_stalnaya.glb` | 43 077 → 14 699 (15 000) | 115 × 30 × 200 | 100 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.53 | ⚠ ширина 115 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `door_wood_vnutrennyaya_idle` | `door_wood_vnutrennyaya.glb` | 43 342 → 14 700 (15 000) | 105 × 44 × 200 | 100 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.50 | — |
| `duct_tape_izolenta_idle` | `duct_tape_izolenta.glb` | 47 938 → 2 940 (3 000) | 9 × 10 × 4 | 10 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.18 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (10 см); высота 4 см  в ОС 10 см |
| `dumpster_zelenyy_idle` | `dumpster_zelenyy.glb` | 45 849 → 7 839 (8 000) | 118 × 79 × 110 | 130 × 110 | ×1.18 | 270° | floor | 1 шт. 2048→1024 | 0.37 | — |
| `electronics_shop_idle` | `electronics_shop.glb` | 39 984 → 14 700 (15 000) | 1000 × 549 × 370 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.77 | ⚠ подогнано по ширине; высота 370 см  в ОС 600 см |
| `ext_bus_stop_b_idle` | `ext_bus_stop_b.glb` | 41 942 → 14 699 (15 000) | 311 × 155 × 260 | 100 × 260 | ×3.11 | 0° | floor | 1 шт. 2048→1024 | 0.63 | ⚠ открытые края (дыры в сетке): 2231 рёбер |
| `ext_bus_stop_c_idle` | `ext_bus_stop_c.glb` | 40 710 → 14 700 (15 000) | 351 × 194 × 260 | 100 × 260 | ×3.51 | 270° | floor | 1 шт. 2048→1024 | 0.60 | — |
| `ext_bus_stop_idle` | `ext_bus_stop.glb` | 38 245 → 14 699 (15 000) | 413 × 186 × 260 | 100 × 260 | ×4.13 | 270° | floor | 1 шт. 2048→1024 | 0.63 | ⚠ открытые края (дыры в сетке): 2099 рёбер |
| `ext_fence_wood_b_idle` | `ext_fence_wood_b.glb` | 46 038 → 14 700 (15 000) | 301 × 28 × 150 | 100 × 150 | ×3.01 | 270° | floor | 1 шт. 2048→1024 | 0.60 | — |
| `ext_fence_wood_idle` | `ext_fence_wood.glb` | 44 504 → 14 700 (15 000) | 273 × 25 × 150 | 100 × 150 | ×2.73 | 270° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `facade_garage_damaged_idle` | `facade_garage_damaged.glb` | 42 083 → 14 699 (15 000) | 295 × 87 × 200 | 100 × 200 | ×2.95 | 270° | floor | 1 шт. 2048→1024 | 0.71 | — |
| `faction_banner_znamya_idle` | `faction_banner_znamya.glb` | 48 316 → 14 700 (15 000) | 84 × 38 × 200 | 60 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.52 | ⚠ ширина 84 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `faction_stockpile_yaschiki_idle` | `faction_stockpile_yaschiki.glb` | 44 725 → 7 839 (8 000) | 200 × 139 × 154 | 200 × 120 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ подогнано по ширине; высота 154 см  в ОС 120 см |
| `farm_barn_b_idle` | `farm_barn_b.glb` | 42 873 → 14 699 (15 000) | 1600 × 1195 × 1266 | 1600 × 600 | ×16 | 270° | floor | 1 шт. 2048→1024 | 0.84 | ⚠ подогнано по ширине; высота 1266 см  в ОС 600 см |
| `farm_barn_idle` | `farm_barn.glb` | 40 550 → 14 700 (15 000) | 1600 × 938 × 1343 | 1600 × 600 | ×16 | 270° | floor | 1 шт. 2048→1024 | 0.77 | ⚠ подогнано по ширине; высота 1343 см  в ОС 600 см |
| `fence_broken_idle` | `fence_broken.glb` | 48 320 → 14 700 (15 000) | 157 × 12 × 150 | 100 × 150 | ×1.57 | 270° | floor | 1 шт. 2048→1024 | 1.09 | — |
| `fence_wire_setka_idle` | `fence_wire_setka.glb` | 45 518 → 14 700 (15 000) | 149 × 11 × 150 | 200 × 150 | ×1.5 | 270° | floor | 1 шт. 2048→1024 | 0.83 | ⚠ ширина 149 см  в ОС 200 см (> 15 %) — записано в DEVIATIONS.md |
| `fertilizer_bag_kompost_idle` | `fertilizer_bag_kompost.glb` | 47 878 → 2 940 (3 000) | 25 × 18 × 35 | 25 × 35 | ×0.35 | 270° | floor | 1 шт. 2048→512 | 0.23 | — |
| `finish_brick_damaged_idle` | `finish_brick_damaged.glb` | 46 616 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.03 | 270° | wall | 1 шт. 2048→1024 | 0.48 | — |
| `finish_metal_damaged_idle` | `finish_metal_damaged.glb` | 48 144 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.02 | 270° | wall | 1 шт. 2048→1024 | 0.38 | — |
| `finish_metal_ok_idle` | `finish_metal_ok.glb` | 44 366 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.06 | 270° | wall | 1 шт. 2048→1024 | 0.26 | — |
| `finish_pegboard_idle` | `finish_pegboard.glb` | 45 886 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.01 | 270° | wall | 1 шт. 2048→1024 | 0.56 | — |
| `finish_plaster_damaged_idle` | `finish_plaster_damaged.glb` | 48 876 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.02 | 270° | wall | 1 шт. 2048→1024 | 0.52 | — |
| `finish_plaster_window_idle` | `finish_plaster_window.glb` | 47 210 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.34 | 270° | wall | 1 шт. 2048→1024 | 0.38 | — |
| `finish_tiles_damaged_idle` | `finish_tiles_damaged.glb` | 40 344 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.22 | 270° | wall | 1 шт. 2048→1024 | 0.53 | — |
| `finish_wallpaper_damaged_idle` | `finish_wallpaper_damaged.glb` | 48 484 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.16 | 270° | wall | 1 шт. 2048→1024 | 0.52 | — |
| `finish_wallpaper_ok_b_idle` | `finish_wallpaper_ok_b.glb` | 45 564 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.37 | — |
| `finish_wallpaper_ok_idle` | `finish_wallpaper_ok.glb` | 48 841 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.01 | 270° | wall | 1 шт. 2048→1024 | 0.46 | — |
| `finish_wallpaper_ruined_idle` | `finish_wallpaper_ruined.glb` | 47 584 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.06 | 270° | wall | 1 шт. 2048→1024 | 0.38 | — |
| `finish_wood_panels_damaged_idle` | `finish_wood_panels_damaged.glb` | 45 872 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.05 | 270° | wall | 1 шт. 2048→1024 | 0.43 | — |
| `fire_station_b_idle` | `fire_station_b.glb` | 40 719 → 14 699 (15 000) | 1400 × 1043 × 1318 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.82 | ⚠ подогнано по ширине; высота 1318 см  в ОС 600 см |
| `fire_station_idle` | `fire_station.glb` | 40 705 → 14 699 (15 000) | 1400 × 709 × 703 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.68 | — |
| `first_aid_kit_domashnyaya_idle` | `first_aid_kit_domashnyaya.glb` | 46 774 → 2 940 (3 000) | 22 × 12 × 18 | 25 × 18 | ×0.219 | 270° | floor | 1 шт. 2048→512 | 0.19 | — |
| `fishing_shop_idle` | `fishing_shop.glb` | 41 523 → 14 699 (15 000) | 800 × 624 × 666 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.94 | — |
| `food_bread_hleb_idle` | `food_bread_hleb.glb` | 47 285 → 2 939 (3 000) | 20 × 25 × 10 | 20 × 10 | ×0.251 | 270° | floor | 1 шт. 2048→512 | 0.17 | — |
| `food_canned_tushenka_idle` | `food_canned_tushenka.glb` | 47 314 → 2 940 (3 000) | 9 × 9 × 10 | 8 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.15 | — |
| `food_grain_pshenitsa_idle` | `food_grain_pshenitsa.glb` | 49 973 → 2 939 (3 000) | 18 × 15 × 15 | 15 × 15 | ×0.18 | 270° | floor | 1 шт. 2048→512 | 0.23 | ⚠ ширина 18 см  в ОС 15 см (> 15 %) — записано в DEVIATIONS.md |
| `fridge_elektricheskiy_idle` | `fridge_elektricheskiy.glb` | 48 912 → 14 698 (15 000) | 110 × 110 × 180 | 70 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ ширина 110 см  в ОС 70 см (> 15 %) — записано в DEVIATIONS.md |
| `fuel_canister_5_l_idle` | `fuel_canister_5_l.glb` | 48 224 → 2 940 (3 000) | 34 × 20 × 45 | 35 × 45 | ×0.45 | 270° | floor | 1 шт. 2048→512 | 0.15 | — |
| `fuel_firewood_polenya_idle` | `fuel_firewood_polenya.glb` | 46 746 → 2 940 (3 000) | 40 × 42 × 22 | 40 × 15 | ×0.417 | 270° | floor | 1 шт. 2048→512 | 0.20 | ⚠ подогнано по ширине; высота 22 см  в ОС 15 см |
| `fuel_generator_portativnyy_idle` | `fuel_generator_portativnyy.glb` | 41 786 → 7 840 (8 000) | 70 × 74 × 60 | 70 × 60 | ×0.737 | 270° | floor | 1 шт. 2048→1024 | 0.48 | — |
| `fuse_box_bytovoy_idle` | `fuse_box_bytovoy.glb` | 46 052 → 2 940 (3 000) | 20 × 17 × 50 | 40 × 50 | ×0.5 | 270° | wall | 1 шт. 2048→512 | 0.14 | ⚠ ширина 20 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `gas_station_b_idle` | `gas_station_b.glb` | 38 100 → 14 700 (15 000) | 1200 × 948 × 832 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.76 | ⚠ подогнано по ширине; высота 832 см  в ОС 600 см |
| `gas_station_idle` | `gas_station.glb` | 40 401 → 14 699 (15 000) | 1400 × 1402 × 1005 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.67 | ⚠ подогнано по ширине; высота 1005 см  в ОС 600 см |
| `grave_mound_holm_idle` | `grave_mound_holm.glb` | 47 648 → 7 840 (8 000) | 150 × 196 × 111 | 150 × 60 | ×1.96 | 0° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ подогнано по ширине; высота 111 см  в ОС 60 см |
| `grow_lamp_fioletovaya_led_idle` | `grow_lamp_fioletovaya_led.glb` | 44 276 → 7 840 (8 000) | 80 × 30 × 60 | 80 × 15 | ×0.8 | 270° | ceiling | 1 шт. 2048→1024 | 0.44 | ⚠ подогнано по ширине; высота 60 см  в ОС 15 см |
| `hangar_b_idle` | `hangar_b.glb` | 41 709 → 14 699 (15 000) | 2400 × 1413 × 1114 | 2400 × 600 | ×24 | 270° | floor | 1 шт. 2048→1024 | 0.90 | ⚠ подогнано по ширине; высота 1114 см  в ОС 600 см |
| `hangar_c_idle` | `hangar_c.glb` | 40 558 → 14 698 (15 000) | 2400 × 1205 × 1304 | 2400 × 600 | ×24 | 270° | floor | 1 шт. 2048→1024 | 0.71 | ⚠ подогнано по ширине; высота 1304 см  в ОС 600 см |
| `hangar_idle` | `hangar.glb` | 39 163 → 14 700 (15 000) | 2400 × 2627 × 1588 | 2400 × 600 | ×26.3 | 270° | floor | 1 шт. 2048→1024 | 0.97 | ⚠ подогнано по ширине; высота 1588 см  в ОС 600 см |
| `hatch_bunker_lyuk_s_kolesom_idle` | `hatch_bunker_lyuk_s_kolesom.glb` | 44 840 → 7 840 (8 000) | 100 × 100 × 30 | 100 × 60 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.42 | ⚠ подогнано по ширине; высота 30 см  в ОС 60 см |
| `house_brick2_b_idle` | `house_brick2_b.glb` | 42 232 → 14 699 (15 000) | 900 × 474 × 914 | 900 × 600 | ×9.14 | 270° | floor | 1 шт. 2048→1024 | 0.90 | — |
| `house_brick2_c_idle` | `house_brick2_c.glb` | 43 224 → 14 700 (15 000) | 900 × 665 × 938 | 900 × 600 | ×9.38 | 270° | floor | 1 шт. 2048→1024 | 0.94 | — |
| `house_brick2_idle` | `house_brick2.glb` | 43 117 → 14 699 (15 000) | 900 × 469 × 956 | 900 × 600 | ×9.56 | 270° | floor | 1 шт. 2048→1024 | 0.92 | — |
| `house_cottage_idle` | `house_cottage.glb` | 44 150 → 14 700 (15 000) | 800 × 544 × 341 | 800 × 600 | ×8 | 90° | floor | 1 шт. 2048→1024 | 0.79 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (800 см); высота 341 см  в ОС 600 см |
| `house_farm_idle` | `house_farm.glb` | 41 894 → 14 700 (15 000) | 1000 × 555 × 673 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.78 | — |
| `house_garage_b_idle` | `house_garage_b.glb` | 42 502 → 14 700 (15 000) | 1200 × 669 × 1034 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.83 | ⚠ подогнано по ширине; высота 1034 см  в ОС 600 см |
| `house_garage_idle` | `house_garage.glb` | 42 101 → 14 699 (15 000) | 1200 × 814 × 560 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.82 | — |
| `house_porch_idle` | `house_porch.glb` | 40 129 → 14 699 (15 000) | 900 × 722 × 642 | 900 × 600 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.88 | — |
| `house_small_b_idle` | `house_small_b.glb` | 43 727 → 14 699 (15 000) | 800 × 494 × 510 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.86 | — |
| `house_small_c_idle` | `house_small_c.glb` | 42 372 → 14 700 (15 000) | 800 × 429 × 464 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.94 | — |
| `house_small_d_idle` | `house_small_d.glb` | 38 215 → 14 699 (15 000) | 800 × 592 × 665 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.77 | — |
| `house_small_idle` | `house_small.glb` | 39 364 → 14 700 (15 000) | 800 × 488 × 640 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.76 | — |
| `house_townhouse_idle` | `house_townhouse.glb` | 41 789 → 14 699 (15 000) | 1000 × 516 × 979 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.99 | ⚠ подогнано по ширине; высота 979 см  в ОС 600 см |
| `house_trailer_b_idle` | `house_trailer_b.glb` | 42 605 → 14 699 (15 000) | 1000 × 422 × 378 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.83 | ⚠ подогнано по ширине; высота 378 см  в ОС 600 см |
| `house_trailer_c_idle` | `house_trailer_c.glb` | 39 895 → 14 699 (15 000) | 1000 × 465 × 405 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.80 | ⚠ подогнано по ширине; высота 405 см  в ОС 600 см |
| `house_trailer_d_idle` | `house_trailer_d.glb` | 41 132 → 14 698 (15 000) | 800 × 386 × 289 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.76 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (800 см); высота 289 см  в ОС 600 см |
| `house_trailer_e_idle` | `house_trailer_e.glb` | 41 249 → 14 699 (15 000) | 600 × 272 × 308 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.63 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 308 см  в ОС 600 см |
| `house_trailer_idle` | `house_trailer.glb` | 39 883 → 14 699 (15 000) | 1000 × 552 × 401 | 1000 × 600 | ×10 | 90° | floor | 1 шт. 2048→1024 | 0.81 | ⚠ подогнано по ширине; высота 401 см  в ОС 600 см |
| `house_two_story_b_idle` | `house_two_story_b.glb` | 43 280 → 14 700 (15 000) | 900 × 613 × 630 | 900 × 600 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.88 | — |
| `house_two_story_idle` | `house_two_story.glb` | 43 127 → 14 699 (15 000) | 900 × 580 × 539 | 900 × 600 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.82 | — |
| `house_wood_b_idle` | `house_wood_b.glb` | 40 907 → 14 700 (15 000) | 220 × 219 × 200 | 100 × 200 | ×2.2 | 270° | floor | 1 шт. 2048→1024 | 0.91 | — |
| `house_wood_c_idle` | `house_wood_c.glb` | 42 459 → 14 699 (15 000) | 320 × 202 × 200 | 100 × 200 | ×3.2 | 270° | floor | 1 шт. 2048→1024 | 0.91 | — |
| `house_wood_d_idle` | `house_wood_d.glb` | 39 438 → 14 700 (15 000) | 900 × 707 × 697 | 900 × 600 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.91 | — |
| `hydro_rack_malaya_idle` | `hydro_rack_malaya.glb` | 38 461 → 14 699 (15 000) | 155 × 63 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.94 | ⚠ ширина 155 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `iron_ore_ruda_idle` | `iron_ore_ruda.glb` | 47 796 → 2 940 (3 000) | 16 × 16 × 12 | 15 × 12 | ×0.163 | 270° | floor | 1 шт. 2048→512 | 0.15 | — |
| `key_generic_obychnyy_idle` | `key_generic_obychnyy.glb` | 49 388 → 2 940 (3 000) | 8 × 3 × 1 | 3 × 8 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (8 см); высота 1 см  в ОС 8 см |
| `kitchen_counter_s_rakovinoy_idle` | `kitchen_counter_s_rakovinoy.glb` | 43 758 → 7 840 (8 000) | 120 × 76 × 128 | 120 × 90 | ×1.28 | 180° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ подогнано по ширине; высота 128 см  в ОС 90 см |
| `ladder_metal_pristennaya_idle` | `ladder_metal_pristennaya.glb` | 48 426 → 14 700 (15 000) | 102 × 20 × 300 | 50 × 300 | ×3 | 0° | floor | 1 шт. 2048→1024 | 0.48 | ⚠ ширина 102 см  в ОС 50 см (> 15 %) — записано в DEVIATIONS.md |
| `lamp_ceiling_lampa_nakalivaniya_idle` | `lamp_ceiling_lampa_nakalivaniya.glb` | 49 416 → 2 940 (3 000) | 20 × 20 × 25 | 30 × 25 | ×0.25 | 270° | ceiling | 1 шт. 2048→512 | 0.14 | ⚠ ширина 20 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `light_switch_klavishnyy_idle` | `light_switch_klavishnyy.glb` | 47 196 → 2 940 (3 000) | 8 × 8 × 12 | 8 × 12 | ×0.12 | 270° | wall | 1 шт. 2048→512 | 0.15 | — |
| `lightbulb_nakalivaniya_idle` | `lightbulb_nakalivaniya.glb` | 49 158 → 2 940 (3 000) | 7 × 7 × 12 | 6 × 12 | ×0.12 | 270° | floor | 1 шт. 2048→512 | 0.15 | ⚠ ширина 7 см  в ОС 6 см (> 15 %) — записано в DEVIATIONS.md |
| `lock_padlock_navesnoy_idle` | `lock_padlock_navesnoy.glb` | 48 137 → 2 939 (3 000) | 7 × 3 × 10 | 6 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.17 | — |
| `locker_metal_sportivnyy_idle` | `locker_metal_sportivnyy.glb` | 44 783 → 14 699 (15 000) | 60 × 67 × 180 | 50 × 180 | ×1.8 | 180° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ ширина 60 см  в ОС 50 см (> 15 %) — записано в DEVIATIONS.md |
| `mall_idle` | `mall.glb` | 42 768 → 14 699 (15 000) | 2400 × 1216 × 1270 | 2400 × 600 | ×24 | 270° | floor | 1 шт. 2048→1024 | 1.04 | ⚠ подогнано по ширине; высота 1270 см  в ОС 600 см |
| `map_paper_karta_rayona_idle` | `map_paper_karta_rayona.glb` | 49 338 → 2 940 (3 000) | 27 × 30 × 5 | 30 × 20 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (30 см); высота 5 см  в ОС 20 см |
| `market_stall_b_idle` | `market_stall_b.glb` | 44 394 → 14 700 (15 000) | 257 × 130 × 230 | 100 × 230 | ×2.57 | 270° | floor | 1 шт. 2048→1024 | 0.61 | — |
| `market_stall_c_idle` | `market_stall_c.glb` | 45 600 → 14 700 (15 000) | 193 × 145 × 230 | 100 × 230 | ×2.3 | 90° | floor | 1 шт. 2048→1024 | 0.63 | — |
| `market_stall_idle` | `market_stall.glb` | 47 244 → 14 698 (15 000) | 220 × 123 × 230 | 100 × 230 | ×2.3 | 270° | floor | 1 шт. 2048→1024 | 0.65 | — |
| `mask_gas_voennyy_idle` | `mask_gas_voennyy.glb` | 47 630 → 2 940 (3 000) | 18 × 33 × 30 | 25 × 30 | ×0.326 | 270° | floor | 1 шт. 2048→512 | 0.17 | ⚠ ширина 18 см  в ОС 25 см (> 15 %) — записано в DEVIATIONS.md |
| `mat_cement_meshok_tsementa_idle` | `mat_cement_meshok_tsementa.glb` | 48 826 → 2 940 (3 000) | 31 × 21 × 40 | 30 × 40 | ×0.4 | 270° | floor | 1 шт. 2048→512 | 0.12 | — |
| `mat_cloth_loskut_idle` | `mat_cloth_loskut.glb` | 48 636 → 2 940 (3 000) | 59 × 50 × 20 | 30 × 20 | ×0.586 | 270° | floor | 1 шт. 2048→512 | 0.17 | ⚠ ширина 59 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `mat_glass_list_stekla_idle` | `mat_glass_list_stekla.glb` | 38 227 → 2 939 (3 000) | 30 × 26 × 9 | 30 × 30 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.17 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (30 см); высота 9 см  в ОС 30 см |
| `mat_log_poleno_idle` | `mat_log_poleno.glb` | 47 584 → 7 840 (8 000) | 120 × 45 × 42 | 120 × 20 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.39 | ⚠ подогнано по ширине; высота 42 см  в ОС 20 см |
| `mat_nails_gvozdi_idle` | `mat_nails_gvozdi.glb` | 49 298 → 2 940 (3 000) | 10 × 8 × 4 | 6 × 4 | ×0.102 | 270° | floor | 1 шт. 2048→512 | 0.24 | ⚠ ширина 10 см  в ОС 6 см (> 15 %) — записано в DEVIATIONS.md |
| `mat_pipe_metal_stalnaya_idle` | `mat_pipe_metal_stalnaya.glb` | 46 292 → 7 840 (8 000) | 100 × 43 × 44 | 100 × 8 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.33 | ⚠ подогнано по ширине; высота 44 см  в ОС 8 см |
| `mat_plank_doska_idle` | `mat_plank_doska.glb` | 43 380 → 7 840 (8 000) | 100 × 46 × 24 | 100 × 10 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.43 | ⚠ подогнано по ширине; высота 24 см  в ОС 10 см |
| `mat_rope_penka_idle` | `mat_rope_penka.glb` | 48 688 → 2 939 (3 000) | 30 × 30 × 19 | 30 × 10 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.18 | ⚠ подогнано по ширине; высота 19 см  в ОС 10 см |
| `mat_rubble_bityy_kirpich_idle` | `mat_rubble_bityy_kirpich.glb` | 48 548 → 2 940 (3 000) | 38 × 36 × 15 | 20 × 15 | ×0.381 | 270° | floor | 1 шт. 2048→512 | 0.18 | ⚠ ширина 38 см  в ОС 20 см (> 15 %) — записано в DEVIATIONS.md |
| `mat_scrap_lom_idle` | `mat_scrap_lom.glb` | 47 242 → 2 976 (3 000) | 25 × 20 × 9 | 25 × 15 | ×0.25 | 270° | floor | 1 шт. 2048→512 | 0.28 | ⚠ подогнано по ширине; высота 9 см  в ОС 15 см |
| `mat_sheet_metal_tonkiy_idle` | `mat_sheet_metal_tonkiy.glb` | 48 778 → 7 840 (8 000) | 100 × 148 × 20 | 100 × 3 | ×1.48 | 270° | floor | 1 шт. 2048→1024 | 0.25 | ⚠ подогнано по ширине; высота 20 см  в ОС 3 см |
| `mat_wire_mednaya_idle` | `mat_wire_mednaya.glb` | 47 889 → 2 939 (3 000) | 20 × 8 × 20 | 20 × 20 | ×0.2 | 270° | floor | 1 шт. 2048→512 | 0.23 | — |
| `meal_soup_ovoschnoy_sup_idle` | `meal_soup_ovoschnoy_sup.glb` | 49 686 → 2 940 (3 000) | 20 × 18 × 10 | 15 × 10 | ×0.199 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ ширина 20 см  в ОС 15 см (> 15 %) — записано в DEVIATIONS.md |
| `meat_cooked_zharenoe_idle` | `meat_cooked_zharenoe.glb` | 47 534 → 2 940 (3 000) | 15 × 8 × 9 | 15 × 8 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.11 | — |
| `meat_raw_krolik_idle` | `meat_raw_krolik.glb` | 48 278 → 2 940 (3 000) | 15 × 8 × 9 | 15 × 8 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.16 | — |
| `medical_kit_polevoy_idle` | `medical_kit_polevoy.glb` | 45 436 → 2 940 (3 000) | 49 × 31 × 25 | 35 × 25 | ×0.487 | 270° | floor | 1 шт. 2048→512 | 0.19 | ⚠ ширина 49 см  в ОС 35 см (> 15 %) — записано в DEVIATIONS.md |
| `medicine_cabinet_vannyy_idle` | `medicine_cabinet_vannyy.glb` | 44 954 → 7 840 (8 000) | 48 × 31 × 60 | 50 × 60 | ×0.6 | 270° | wall | 1 шт. 2048→1024 | 0.32 | — |
| `metro_idle` | `metro.glb` | 38 710 → 14 700 (15 000) | 1000 × 845 × 707 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.96 | — |
| `mine_b_idle` | `mine_b.glb` | 42 370 → 14 700 (15 000) | 1400 × 1315 × 1366 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.89 | ⚠ подогнано по ширине; высота 1366 см  в ОС 600 см |
| `mine_c_idle` | `mine_c.glb` | 42 304 → 14 698 (15 000) | 1400 × 1496 × 1374 | 1400 × 600 | ×15 | 270° | floor | 1 шт. 2048→1024 | 0.96 | ⚠ подогнано по ширине; высота 1374 см  в ОС 600 см |
| `mine_cart_empty_idle` | `mine_cart_empty.glb` | 42 514 → 7 840 (8 000) | 248 × 131 × 120 | 100 × 120 | ×2.48 | 270° | floor | 1 шт. 2048→1024 | 0.49 | — |
| `mine_cart_ore_idle` | `mine_cart_ore.glb` | 45 936 → 7 840 (8 000) | 212 × 120 × 120 | 100 × 120 | ×2.12 | 90° | floor | 1 шт. 2048→1024 | 0.40 | — |
| `mine_cart_wood_idle` | `mine_cart_wood.glb` | 43 072 → 7 840 (8 000) | 237 × 140 × 120 | 100 × 120 | ×2.37 | 0° | floor | 1 шт. 2048→1024 | 0.46 | — |
| `mine_crate_dynamite_idle` | `mine_crate_dynamite.glb` | 44 520 → 7 840 (8 000) | 56 × 70 × 60 | 100 × 60 | ×0.702 | 270° | floor | 1 шт. 2048→1024 | 0.43 | — |
| `mine_crate_idle` | `mine_crate.glb` | 44 216 → 7 840 (8 000) | 112 × 70 × 60 | 100 × 60 | ×1.12 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `mine_crates_stack_b_idle` | `mine_crates_stack_b.glb` | 43 651 → 14 699 (15 000) | 100 × 111 × 150 | 100 × 150 | ×1.5 | 0° | floor | 1 шт. 2048→1024 | 0.70 | — |
| `mine_crates_stack_idle` | `mine_crates_stack.glb` | 45 744 → 14 700 (15 000) | 117 × 94 × 150 | 100 × 150 | ×1.5 | 270° | floor | 1 шт. 2048→1024 | 0.77 | — |
| `mine_floodlight_b_idle` | `mine_floodlight_b.glb` | 47 086 → 14 700 (15 000) | 89 × 102 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.52 | — |
| `mine_floodlight_c_idle` | `mine_floodlight_c.glb` | 47 086 → 14 700 (15 000) | 89 × 102 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.52 | — |
| `mine_floodlight_idle` | `mine_floodlight.glb` | 48 480 → 14 700 (15 000) | 88 × 94 × 180 | 100 × 180 | ×1.8 | 180° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `mine_idle` | `mine.glb` | 46 310 → 14 700 (15 000) | 1400 × 1557 × 1305 | 1400 × 600 | ×15.6 | 270° | floor | 1 шт. 2048→1024 | 0.80 | ⚠ подогнано по ширине; высота 1305 см  в ОС 600 см |
| `mine_ladder_b_idle` | `mine_ladder_b.glb` | 48 162 → 14 700 (15 000) | 173 × 713 × 300 | 100 × 300 | ×7.13 | 270° | floor | 1 шт. 2048→1024 | 0.51 | — |
| `mine_ladder_idle` | `mine_ladder.glb` | 46 892 → 14 700 (15 000) | 99 × 202 × 300 | 100 × 300 | ×3 | 270° | floor | 1 шт. 2048→1024 | 0.50 | — |
| `mine_lamp_cage_idle` | `mine_lamp_cage.glb` | 45 813 → 7 839 (8 000) | 17 × 17 × 40 | 100 × 40 | ×0.4 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `mine_lamp_string_idle` | `mine_lamp_string.glb` | 48 180 → 7 840 (8 000) | 118 × 14 × 60 | 100 × 60 | ×1.18 | 270° | floor | 1 шт. 2048→1024 | 0.54 | — |
| `mine_lantern_b_idle` | `mine_lantern_b.glb` | 48 288 → 7 840 (8 000) | 17 × 12 × 35 | 100 × 35 | ×0.35 | 90° | floor | 1 шт. 2048→1024 | 0.44 | — |
| `mine_lantern_idle` | `mine_lantern.glb` | 47 902 → 7 840 (8 000) | 16 × 12 × 35 | 100 × 35 | ×0.35 | 90° | floor | 1 шт. 2048→1024 | 0.45 | — |
| `mine_ore_pile_idle` | `mine_ore_pile.glb` | 49 850 → 7 840 (8 000) | 162 × 141 × 80 | 100 × 80 | ×1.62 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `mine_post_wood_idle` | `mine_post_wood.glb` | 48 516 → 14 700 (15 000) | 58 × 65 × 250 | 100 × 250 | ×2.5 | 270° | floor | 1 шт. 2048→1024 | 0.47 | — |
| `mine_rails_end_idle` | `mine_rails_end.glb` | 44 627 → 7 839 (8 000) | 150 × 76 × 41 | 150 × 150 | ×1.5 | 270° | floor | 1 шт. 2048→1024 | 0.53 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (150 см); высота 41 см  в ОС 150 см |
| `mine_rails_straight_idle` | `mine_rails_straight.glb` | 44 712 → 7 840 (8 000) | 300 × 149 × 37 | 300 × 150 | ×3 | 0° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ подогнано по ширине; высота 37 см  в ОС 150 см |
| `mine_support_wood_idle` | `mine_support_wood.glb` | 47 110 → 14 698 (15 000) | 253 × 137 × 250 | 100 × 250 | ×2.53 | 270° | floor | 1 шт. 2048→1024 | 0.58 | — |
| `mine_tool_rack_idle` | `mine_tool_rack.glb` | 47 236 → 14 700 (15 000) | 159 × 68 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.63 | — |
| `mine_wall_mesh_idle` | `mine_wall_mesh.glb` | 48 232 → 16 090 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.07 | 270° | wall | 1 шт. 2048→1024 | 1.21 | ⚠ не удалось облегчить до лимита: 16090 |
| `mine_wall_planks_idle` | `mine_wall_planks.glb` | 45 222 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.06 | 270° | wall | 1 шт. 2048→1024 | 0.45 | — |
| `mine_wall_planks_stone_b_idle` | `mine_wall_planks_stone_b.glb` | 45 450 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.11 | 270° | wall | 1 шт. 2048→1024 | 0.49 | — |
| `mine_wall_planks_stone_idle` | `mine_wall_planks_stone.glb` | 45 659 → 7 839 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.08 | 270° | wall | 1 шт. 2048→1024 | 0.52 | — |
| `mine_wall_rock_idle` | `mine_wall_rock.glb` | 47 205 → 7 838 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.18 | 270° | wall | 1 шт. 2048→1024 | 0.42 | — |
| `mine_wall_rock_ore_idle` | `mine_wall_rock_ore.glb` | 49 738 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.06 | 270° | wall | 1 шт. 2048→1024 | 0.35 | — |
| `motel_b_idle` | `motel_b.glb` | 40 305 → 14 699 (15 000) | 1600 × 592 × 340 | 1600 × 600 | ×16 | 270° | floor | 1 шт. 2048→1024 | 0.57 | ⚠ подогнано по ширине; высота 340 см  в ОС 600 см |
| `motel_idle` | `motel.glb` | 39 015 → 14 699 (15 000) | 2000 × 807 × 528 | 2000 × 600 | ×20 | 270° | floor | 1 шт. 2048→1024 | 0.69 | — |
| `motorcycle_b_idle` | `motorcycle_b.glb` | 47 496 → 7 838 (8 000) | 210 × 82 × 114 | 210 × 150 | ×2.1 | 90° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `motorcycle_idle` | `motorcycle.glb` | 47 407 → 7 839 (8 000) | 210 × 84 × 116 | 210 × 150 | ×2.1 | 90° | floor | 1 шт. 2048→1024 | 0.54 | — |
| `motorhome_idle` | `motorhome.glb` | 40 991 → 7 839 (8 000) | 700 × 290 × 348 | 700 × 150 | ×7 | 0° | floor | 1 шт. 2048→1024 | 0.56 | ⚠ подогнано по ширине; высота 348 см  в ОС 150 см |
| `mutant_crawler_polzun_idle` | `mutant_crawler_polzun.glb` | 47 442 → 14 700 (15 000) | 140 × 164 × 131 | 140 × 60 | ×1.64 | 270° | floor | 1 шт. 2048→1024 | 0.55 | ⚠ подогнано по ширине; высота 131 см  в ОС 60 см |
| `note_diary_zapiska_idle` | `note_diary_zapiska.glb` | 47 392 → 2 940 (3 000) | 20 × 16 × 7 | 15 × 20 | ×0.2 | 270° | floor | 1 шт. 2048→512 | 0.19 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (20 см); высота 7 см  в ОС 20 см |
| `noticeboard_derevyannaya_idle` | `noticeboard_derevyannaya.glb` | 45 044 → 7 840 (8 000) | 62 × 21 × 80 | 100 × 80 | ×0.8 | 270° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ ширина 62 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `nuclear_plant_b_idle` | `nuclear_plant_b.glb` | 45 288 → 14 698 (15 000) | 2400 × 1014 × 1314 | 2400 × 600 | ×24 | 270° | floor | 1 шт. 2048→1024 | 0.82 | ⚠ подогнано по ширине; высота 1314 см  в ОС 600 см |
| `nuclear_plant_idle` | `nuclear_plant.glb` | 45 713 → 14 700 (15 000) | 2400 × 1508 × 1314 | 2400 × 600 | ×24 | 270° | floor | 1 шт. 2048→1024 | 0.91 | ⚠ подогнано по ширине; высота 1314 см  в ОС 600 см |
| `painkiller_tabletki_idle` | `painkiller_tabletki.glb` | 47 490 → 2 940 (3 000) | 5 × 5 × 8 | 6 × 8 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.19 | ⚠ ширина 5 см  в ОС 6 см (> 15 %) — записано в DEVIATIONS.md |
| `part_electronic_platy_idle` | `part_electronic_platy.glb` | 44 026 → 2 940 (3 000) | 10 × 10 × 1 | 10 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.29 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (10 см); высота 1 см  в ОС 10 см |
| `part_mech_shesterni_idle` | `part_mech_shesterni.glb` | 48 173 → 2 940 (3 000) | 15 × 12 × 7 | 15 × 15 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.25 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (15 см); высота 7 см  в ОС 15 см |
| `part_rare_circuit_voennaya_plata_idle` | `part_rare_circuit_voennaya_plata.glb` | 44 598 → 2 940 (3 000) | 8 × 10 × 1 | 10 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.27 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (10 см); высота 1 см  в ОС 10 см |
| `pickup_b_idle` | `pickup_b.glb` | 43 458 → 7 840 (8 000) | 520 × 234 × 191 | 520 × 150 | ×5.2 | 90° | floor | 1 шт. 2048→1024 | 0.45 | ⚠ подогнано по ширине; высота 191 см  в ОС 150 см |
| `pickup_idle` | `pickup.glb` | 43 763 → 7 839 (8 000) | 520 × 216 × 178 | 520 × 150 | ×5.2 | 0° | floor | 1 шт. 2048→1024 | 0.44 | — |
| `plant_potato_kartofel_idle` | `plant_potato_kartofel.glb` | 48 470 → 2 940 (3 000) | 37 × 36 × 40 | 40 × 40 | ×0.4 | 270° | floor | 1 шт. 2048→512 | 0.21 | — |
| `plant_tree_sosna_idle` | `plant_tree_sosna.glb` | 47 110 → 14 698 (15 000) | 234 × 207 × 450 | 160 × 450 | ×4.5 | 270° | floor | 1 шт. 2048→1024 | 0.64 | ⚠ ширина 234 см  в ОС 160 см (> 15 %) — записано в DEVIATIONS.md |
| `plant_wheat_pshenitsa_idle` | `plant_wheat_pshenitsa.glb` | 44 918 → 7 839 (8 000) | 120 × 97 × 80 | 50 × 80 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.70 | ⚠ ширина 120 см  в ОС 50 см (> 15 %) — записано в DEVIATIONS.md |
| `planter_box_derevyannyy_yaschik_idle` | `planter_box_derevyannyy_yaschik.glb` | 44 360 → 7 840 (8 000) | 120 × 55 × 39 | 120 × 40 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.46 | — |
| `poison_vial_slabyy_idle` | `poison_vial_slabyy.glb` | 49 248 → 2 940 (3 000) | 5 × 5 × 10 | 5 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.18 | — |
| `police_station_b_idle` | `police_station_b.glb` | 40 669 → 14 699 (15 000) | 1200 × 585 × 1004 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.94 | ⚠ подогнано по ширине; высота 1004 см  в ОС 600 см |
| `police_station_idle` | `police_station.glb` | 41 836 → 14 700 (15 000) | 1200 × 617 × 555 | 1200 × 600 | ×12 | 270° | floor | 1 шт. 2048→1024 | 0.99 | — |
| `power_cable_tonkiy_idle` | `power_cable_tonkiy.glb` | 49 106 → 2 940 (3 000) | 20 × 7 × 20 | 20 × 20 | ×0.2 | 0° | floor | 1 шт. 2048→512 | 0.24 | — |
| `power_plant_b_idle` | `power_plant_b.glb` | 43 270 → 14 700 (15 000) | 2000 × 1228 × 1456 | 2000 × 600 | ×20 | 270° | floor | 1 шт. 2048→1024 | 0.98 | ⚠ подогнано по ширине; высота 1456 см  в ОС 600 см |
| `power_plant_idle` | `power_plant.glb` | 45 782 → 14 700 (15 000) | 2000 × 1054 × 1100 | 2000 × 600 | ×20 | 90° | floor | 1 шт. 2048→1024 | 1.08 | ⚠ подогнано по ширине; высота 1100 см  в ОС 600 см |
| `prison_armory_cage_idle` | `prison_armory_cage.glb` | 43 480 → 17 660 (15 000) | 600 × 409 × 414 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 1.57 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 414 см  в ОС 600 см<br>⚠ не удалось облегчить до лимита: 17660 |
| `prison_armory_locker_b_idle` | `prison_armory_locker_b.glb` | 43 339 → 14 699 (15 000) | 89 × 59 × 190 | 100 × 190 | ×1.9 | 270° | floor | 1 шт. 2048→1024 | 0.51 | — |
| `prison_armory_locker_idle` | `prison_armory_locker.glb` | 47 058 → 14 700 (15 000) | 98 × 67 × 190 | 100 × 190 | ×1.9 | 270° | floor | 1 шт. 2048→1024 | 0.52 | — |
| `prison_armory_open_idle` | `prison_armory_open.glb` | 47 222 → 14 698 (15 000) | 176 × 89 × 190 | 100 × 190 | ×1.9 | 180° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `prison_bunk_idle` | `prison_bunk.glb` | 40 461 → 14 699 (15 000) | 197 × 119 × 180 | 100 × 180 | ×1.97 | 270° | floor | 1 шт. 2048→1024 | 0.53 | — |
| `prison_cell_bars_idle` | `prison_cell_bars.glb` | 44 777 → 14 699 (15 000) | 307 × 33 × 250 | 100 × 250 | ×3.07 | 270° | floor | 1 шт. 2048→1024 | 0.60 | — |
| `prison_fence_wire_idle` | `prison_fence_wire.glb` | 46 340 → 14 699 (15 000) | 361 × 54 × 300 | 100 × 300 | ×3.61 | 270° | floor | 1 шт. 2048→1024 | 1.22 | — |
| `prison_guard_booth_b_idle` | `prison_guard_booth_b.glb` | 43 464 → 14 700 (15 000) | 323 × 192 × 300 | 100 × 300 | ×3.23 | 270° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `prison_guard_booth_c_idle` | `prison_guard_booth_c.glb` | 39 088 → 14 700 (15 000) | 261 × 263 × 300 | 100 × 300 | ×3 | 270° | floor | 1 шт. 2048→1024 | 0.57 | ⚠ открытые края (дыры в сетке): 1540 рёбер |
| `prison_guard_booth_idle` | `prison_guard_booth.glb` | 44 871 → 14 699 (15 000) | 158 × 108 × 300 | 100 × 300 | ×3 | 90° | floor | 1 шт. 2048→1024 | 0.67 | — |
| `prison_locker_row_idle` | `prison_locker_row.glb` | 43 181 → 14 699 (15 000) | 55 × 56 × 190 | 100 × 190 | ×1.9 | 270° | floor | 1 шт. 2048→1024 | 0.48 | — |
| `prison_rack_batons_idle` | `prison_rack_batons.glb` | 46 540 → 7 840 (8 000) | 127 × 33 × 120 | 100 × 120 | ×1.27 | 270° | floor | 1 шт. 2048→1024 | 0.41 | — |
| `prison_toilet_sink_idle` | `prison_toilet_sink.glb` | 45 220 → 7 840 (8 000) | 55 × 85 × 110 | 100 × 110 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.35 | — |
| `prison_wall_cell_idle` | `prison_wall_cell.glb` | 48 397 → 7 839 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.59 | — |
| `prison_wall_mesh_idle` | `prison_wall_mesh.glb` | 42 554 → 7 840 (8 000) | 100 × 10 × 100 | 100 × 100 | ×1.22 | 270° | wall | 1 шт. 2048→1024 | 0.61 | — |
| `prison_watchtower_b_idle` | `prison_watchtower_b.glb` | 44 871 → 14 699 (15 000) | 306 × 298 × 900 | 100 × 900 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.61 | — |
| `prison_watchtower_c_idle` | `prison_watchtower_c.glb` | 43 453 → 14 699 (15 000) | 314 × 321 × 900 | 100 × 900 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.76 | — |
| `prison_watchtower_idle` | `prison_watchtower.glb` | 42 426 → 14 700 (15 000) | 306 × 228 × 900 | 100 × 900 | ×9 | 270° | floor | 1 шт. 2048→1024 | 0.73 | — |
| `pyre_pile_koster_idle` | `pyre_pile_koster.glb` | 47 020 → 7 840 (8 000) | 150 × 103 × 57 | 150 × 80 | ×1.5 | 270° | floor | 1 шт. 2048→1024 | 0.43 | ⚠ подогнано по ширине; высота 57 см  в ОС 80 см |
| `rabbit_wild_krolik_idle` | `rabbit_wild_krolik.glb` | 49 230 → 14 700 (15 000) | 13 × 16 × 25 | 35 × 25 | ×0.25 | 270° | floor | 1 шт. 2048→1024 | 0.54 | ⚠ ширина 13 см  в ОС 35 см (> 15 %) — записано в DEVIATIONS.md |
| `rack_metal_s_3_polkami_idle` | `rack_metal_s_3_polkami.glb` | 44 388 → 14 700 (15 000) | 115 × 53 × 200 | 120 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 1.04 | — |
| `radio_desk_nastolnyy_idle` | `radio_desk_nastolnyy.glb` | 46 666 → 2 940 (3 000) | 34 × 19 × 25 | 35 × 25 | ×0.338 | 270° | floor | 1 шт. 2048→512 | 0.17 | — |
| `radio_tower_idle` | `radio_tower.glb` | 45 684 → 14 700 (15 000) | 411 × 450 × 1500 | 100 × 1500 | ×15 | 270° | floor | 1 шт. 2048→1024 | 0.75 | — |
| `raider_human_maroder_idle` | `raider_human_maroder.glb` | 48 046 → 14 698 (15 000) | 178 × 36 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.64 | ⚠ ширина 178 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `rain_collector_plenka_i_zhelob_idle` | `rain_collector_plenka_i_zhelob.glb` | 45 088 → 14 700 (15 000) | 110 × 83 × 83 | 110 × 60 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.64 | ⚠ подогнано по ширине; высота 83 см  в ОС 60 см |
| `rat_pest_krysa_idle` | `rat_pest_krysa.glb` | 48 422 → 14 700 (15 000) | 25 × 44 × 31 | 25 × 10 | ×0.44 | 270° | floor | 1 шт. 2048→1024 | 0.91 | ⚠ подогнано по ширине; высота 31 см  в ОС 10 см |
| `ration_dry_armeyskiy_idle` | `ration_dry_armeyskiy.glb` | 48 294 → 2 940 (3 000) | 15 × 8 × 4 | 15 × 10 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.12 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (15 см); высота 4 см  в ОС 10 см |
| `recycler_bench_ruchnoy_idle` | `recycler_bench_ruchnoy.glb` | 43 646 → 7 840 (8 000) | 130 × 75 × 98 | 130 × 95 | ×1.3 | 0° | floor | 1 шт. 2048→1024 | 0.56 | — |
| `repair_kit_malyy_nabor_idle` | `repair_kit_malyy_nabor.glb` | 45 698 → 2 940 (3 000) | 25 × 19 × 26 | 25 × 15 | ×0.256 | 270° | floor | 1 шт. 2048→512 | 0.18 | ⚠ подогнано по ширине; высота 26 см  в ОС 15 см |
| `ruin_column_idle` | `ruin_column.glb` | 48 272 → 14 700 (15 000) | 92 × 99 × 300 | 100 × 300 | ×3 | 270° | floor | 1 шт. 2048→1024 | 0.53 | — |
| `ruin_pipe_burst_idle` | `ruin_pipe_burst.glb` | 47 706 → 7 840 (8 000) | 235 × 167 × 100 | 100 × 100 | ×2.35 | 270° | floor | 1 шт. 2048→1024 | 0.42 | ⚠ 2 отдельн. крупн. кус(ка/ков) в стороне от главного — возможно  лишняя вещь с картинки (рюкзак  ящик…) — посмотреть на превью |
| `ruin_pipe_wall_idle` | `ruin_pipe_wall.glb` | 45 677 → 14 699 (15 000) | 369 × 193 × 200 | 100 × 200 | ×3.69 | 270° | floor | 1 шт. 2048→1024 | 0.81 | — |
| `safe_metal_nastennyy_idle` | `safe_metal_nastennyy.glb` | 43 477 → 7 839 (8 000) | 50 × 70 × 60 | 50 × 60 | ×0.701 | 180° | floor | 1 шт. 2048→1024 | 0.35 | — |
| `school_b_idle` | `school_b.glb` | 40 637 → 14 699 (15 000) | 2000 × 1161 × 1255 | 2000 × 600 | ×20 | 270° | floor | 1 шт. 2048→1024 | 0.95 | ⚠ подогнано по ширине; высота 1255 см  в ОС 600 см |
| `school_idle` | `school.glb` | 42 646 → 14 700 (15 000) | 2000 × 1486 × 797 | 2000 × 600 | ×20 | 270° | floor | 1 шт. 2048→1024 | 1.27 | ⚠ подогнано по ширине; высота 797 см  в ОС 600 см |
| `scrap_pile_metallolom_idle` | `scrap_pile_metallolom.glb` | 49 188 → 7 840 (8 000) | 120 × 108 × 80 | 120 × 80 | ×1.2 | 270° | floor | 1 шт. 2048→1024 | 0.54 | — |
| `seed_bag_kartofel_idle` | `seed_bag_kartofel.glb` | 48 055 → 2 939 (3 000) | 8 × 5 × 14 | 10 × 14 | ×0.14 | 270° | floor | 1 шт. 2048→512 | 0.13 | ⚠ ширина 8 см  в ОС 10 см (> 15 %) — записано в DEVIATIONS.md |
| `sewing_table_ruchnaya_mashina_idle` | `sewing_table_ruchnaya_mashina.glb` | 43 066 → 7 840 (8 000) | 110 × 57 × 110 | 110 × 85 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.46 | ⚠ подогнано по ширине; высота 110 см  в ОС 85 см |
| `shack_brick_idle` | `shack_brick.glb` | 41 464 → 14 700 (15 000) | 600 × 458 × 396 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.80 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 396 см  в ОС 600 см |
| `shack_wood_idle` | `shack_wood.glb` | 43 847 → 14 699 (15 000) | 600 × 353 × 445 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.99 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 445 см  в ОС 600 см |
| `shelf_wood_derevyannaya_idle` | `shelf_wood_derevyannaya.glb` | 46 406 → 7 840 (8 000) | 100 × 40 × 87 | 100 × 30 | ×1 | 270° | wall | 1 шт. 2048→1024 | 0.35 | ⚠ подогнано по ширине; высота 87 см  в ОС 30 см |
| `shelter_panel_prostoy_pult_idle` | `shelter_panel_prostoy_pult.glb` | 47 074 → 7 840 (8 000) | 84 × 29 × 70 | 60 × 70 | ×0.84 | 270° | wall | 1 шт. 2048→1024 | 0.39 | ⚠ ширина 84 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `shop_cafe_bld_idle` | `shop_cafe_bld.glb` | 46 540 → 14 700 (15 000) | 1000 × 987 × 639 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.78 | — |
| `shop_general_idle` | `shop_general.glb` | 42 849 → 14 699 (15 000) | 800 × 388 × 525 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.83 | — |
| `shop_grocery_bld_idle` | `shop_grocery_bld.glb` | 39 834 → 14 700 (15 000) | 1000 × 543 × 487 | 1000 × 600 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.95 | — |
| `shop_pharmacy_bld_idle` | `shop_pharmacy_bld.glb` | 40 316 → 14 698 (15 000) | 800 × 396 × 467 | 800 × 600 | ×8 | 270° | floor | 1 шт. 2048→1024 | 0.83 | — |
| `sign_diner_b_idle` | `sign_diner_b.glb` | 46 896 → 14 700 (15 000) | 352 × 74 × 500 | 100 × 500 | ×5 | 270° | floor | 1 шт. 2048→1024 | 0.61 | — |
| `sign_diner_c_idle` | `sign_diner_c.glb` | 45 622 → 14 700 (15 000) | 250 × 44 × 500 | 100 × 500 | ×5 | 270° | floor | 1 шт. 2048→1024 | 0.63 | — |
| `sign_diner_d_idle` | `sign_diner_d.glb` | 42 562 → 14 700 (15 000) | 114 × 24 × 200 | 100 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.58 | — |
| `sign_diner_idle` | `sign_diner.glb` | 48 454 → 14 700 (15 000) | 324 × 45 × 500 | 100 × 500 | ×5 | 270° | floor | 1 шт. 2048→1024 | 0.64 | — |
| `sign_letters_diner_idle` | `sign_letters_diner.glb` | 44 512 → 7 840 (8 000) | 460 × 26 × 120 | 100 × 120 | ×4.6 | 270° | floor | 1 шт. 2048→1024 | 0.46 | ⚠ 4 отдельн. крупн. кус(ка/ков) в стороне от главного — возможно  лишняя вещь с картинки (рюкзак  ящик…) — посмотреть на превью |
| `sign_motel_b_idle` | `sign_motel_b.glb` | 46 056 → 14 700 (15 000) | 245 × 43 × 600 | 100 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.59 | — |
| `sign_motel_idle` | `sign_motel.glb` | 45 262 → 14 700 (15 000) | 349 × 70 × 600 | 100 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.58 | — |
| `signpost_fork_dorozhnyy_znak_idle` | `signpost_fork_dorozhnyy_znak.glb` | 46 770 → 14 700 (15 000) | 148 × 27 × 220 | 80 × 220 | ×2.2 | 270° | floor | 1 шт. 2048→1024 | 0.52 | ⚠ ширина 148 см  в ОС 80 см (> 15 %) — записано в DEVIATIONS.md |
| `sink_tap_kuhonnaya_idle` | `sink_tap_kuhonnaya.glb` | 43 728 → 7 840 (8 000) | 44 × 49 × 90 | 80 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.35 | ⚠ ширина 44 см  в ОС 80 см (> 15 %) — записано в DEVIATIONS.md |
| `soap_kusok_myla_idle` | `soap_kusok_myla.glb` | 49 002 → 2 940 (3 000) | 8 × 6 × 3 | 8 × 4 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.12 | — |
| `soil_clump_chernozem_idle` | `soil_clump_chernozem.glb` | 47 788 → 2 940 (3 000) | 15 × 14 × 5 | 15 × 12 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.17 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (15 см); высота 5 см  в ОС 12 см |
| `solar_panel_malaya_100_vt_idle` | `solar_panel_malaya_100_vt.glb` | 46 416 → 14 700 (15 000) | 52 × 46 × 80 | 120 × 80 | ×0.8 | 270° | floor | 1 шт. 2048→1024 | 0.51 | ⚠ ширина 52 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `splint_gotovaya_idle` | `splint_gotovaya.glb` | 47 824 → 2 940 (3 000) | 40 × 18 × 14 | 40 × 8 | ×0.4 | 0° | floor | 1 шт. 2048→512 | 0.18 | ⚠ подогнано по ширине; высота 14 см  в ОС 8 см |
| `stairs_wood_derevyannaya_idle` | `stairs_wood_derevyannaya.glb` | 40 028 → 14 700 (15 000) | 288 × 162 × 260 | 110 × 260 | ×2.88 | 270° | floor | 1 шт. 2048→1024 | 0.48 | ⚠ ширина 288 см  в ОС 110 см (> 15 %) — записано в DEVIATIONS.md |
| `stone_chunk_bulyzhnik_idle` | `stone_chunk_bulyzhnik.glb` | 48 506 → 2 940 (3 000) | 15 × 10 × 5 | 15 × 12 | ×0.15 | 270° | floor | 1 шт. 2048→512 | 0.12 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (15 см); высота 5 см  в ОС 12 см |
| `stove_cook_gazovaya_idle` | `stove_cook_gazovaya.glb` | 44 085 → 7 839 (8 000) | 66 × 69 × 90 | 70 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.41 | — |
| `stove_heat_stalnaya_bochka_idle` | `stove_heat_stalnaya_bochka.glb` | 47 802 → 7 840 (8 000) | 37 × 71 × 90 | 60 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ ширина 37 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `street_lamp_tselyy_idle` | `street_lamp_tselyy.glb` | 46 579 → 14 699 (15 000) | 97 × 98 × 400 | 30 × 400 | ×4 | 270° | floor | 1 шт. 2048→1024 | 0.53 | ⚠ ширина 97 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `supermarket_idle` | `supermarket.glb` | 36 812 → 14 700 (15 000) | 2000 × 864 × 662 | 2000 × 600 | ×20 | 270° | floor | 1 шт. 2048→1024 | 0.76 | — |
| `survivor_base_igrok_idle` | `survivor_base_igrok.glb` | 47 572 → 14 700 (15 000) | 100 × 36 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.53 | — |
| `table_wood_obedennyy_idle` | `table_wood_obedennyy.glb` | 44 742 → 7 840 (8 000) | 139 × 84 × 75 | 120 × 75 | ×1.39 | 0° | floor | 1 шт. 2048→1024 | 0.35 | ⚠ ширина 139 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `tank_water_plastikovyy_1000_l_idle` | `tank_water_plastikovyy_1000_l.glb` | 41 445 → 14 699 (15 000) | 188 × 198 × 190 | 160 × 190 | ×1.98 | 270° | floor | 1 шт. 2048→1024 | 0.71 | ⚠ ширина 188 см  в ОС 160 см (> 15 %) — записано в DEVIATIONS.md |
| `tent_big_idle` | `tent_big.glb` | 49 345 → 14 699 (15 000) | 806 × 692 × 400 | 100 × 400 | ×8.06 | 90° | floor | 1 шт. 2048→1024 | 0.57 | — |
| `tent_camp_aframe_idle` | `tent_camp_aframe.glb` | 45 077 → 7 839 (8 000) | 245 × 200 × 140 | 100 × 140 | ×2.45 | 270° | floor | 1 шт. 2048→1024 | 0.39 | — |
| `tent_camp_odnomestnaya_idle` | `tent_camp_odnomestnaya.glb` | 45 509 → 14 699 (15 000) | 240 × 222 × 140 | 220 × 140 | ×2.4 | 270° | floor | 1 шт. 2048→1024 | 0.56 | — |
| `tent_dome_idle` | `tent_dome.glb` | 46 136 → 7 840 (8 000) | 240 × 216 × 130 | 100 × 130 | ×2.4 | 270° | floor | 1 шт. 2048→1024 | 0.36 | — |
| `tent_greenhouse_b_idle` | `tent_greenhouse_b.glb` | 46 242 → 14 700 (15 000) | 600 × 599 × 319 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.61 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 319 см  в ОС 600 см |
| `tent_greenhouse_idle` | `tent_greenhouse.glb` | 46 242 → 14 700 (15 000) | 600 × 599 × 319 | 600 × 600 | ×6 | 270° | floor | 1 шт. 2048→1024 | 0.61 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (600 см); высота 319 см  в ОС 600 см |
| `tent_military_idle` | `tent_military.glb` | 47 444 → 14 699 (15 000) | 569 × 399 × 250 | 100 × 250 | ×5.69 | 270° | floor | 1 шт. 2048→1024 | 0.57 | ⚠ открытые края (дыры в сетке): 3354 рёбер |
| `toilet_fayansovyy_so_smyvom_idle` | `toilet_fayansovyy_so_smyvom.glb` | 45 230 → 7 840 (8 000) | 48 × 72 × 75 | 40 × 75 | ×0.75 | 180° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ ширина 48 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `tool_axe_kolun_idle` | `tool_axe_kolun.glb` | 49 454 → 7 840 (8 000) | 47 × 50 × 60 | 35 × 60 | ×0.6 | 270° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ ширина 47 см  в ОС 35 см (> 15 %) — записано в DEVIATIONS.md |
| `tool_can_opener_ruchnoy_idle` | `tool_can_opener_ruchnoy.glb` | 48 968 → 2 940 (3 000) | 15 × 42 × 5 | 15 × 8 | ×0.416 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ подогнано по ширине; высота 5 см  в ОС 8 см |
| `tool_crowbar_stalnoy_idle` | `tool_crowbar_stalnoy.glb` | 48 236 → 7 840 (8 000) | 70 × 47 × 9 | 70 × 8 | ×0.7 | 270° | floor | 1 шт. 2048→1024 | 0.33 | — |
| `tool_flashlight_ruchnoy_idle` | `tool_flashlight_ruchnoy.glb` | 48 620 → 2 940 (3 000) | 25 × 9 × 9 | 10 × 25 | ×0.25 | 270° | floor | 1 шт. 2048→512 | 0.15 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (25 см); высота 9 см  в ОС 25 см |
| `tool_hammer_stolyarnyy_idle` | `tool_hammer_stolyarnyy.glb` | 49 224 → 2 940 (3 000) | 30 × 10 × 6 | 30 × 10 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.13 | ⚠ подогнано по ширине; высота 6 см  в ОС 10 см |
| `tool_knife_kuhonnyy_idle` | `tool_knife_kuhonnyy.glb` | 47 206 → 2 940 (3 000) | 25 × 23 × 47 | 25 × 5 | ×0.465 | 270° | floor | 1 шт. 2048→512 | 0.13 | ⚠ подогнано по ширине; высота 47 см  в ОС 5 см |
| `tool_lockpick_nabor_idle` | `tool_lockpick_nabor.glb` | 48 290 → 2 940 (3 000) | 10 × 7 × 3 | 10 × 5 | ×0.1 | 0° | floor | 1 шт. 2048→512 | 0.16 | ⚠ подогнано по ширине; высота 3 см  в ОС 5 см |
| `tool_pickaxe_stalnaya_idle` | `tool_pickaxe_stalnaya.glb` | 48 978 → 7 840 (8 000) | 46 × 60 × 28 | 35 × 60 | ×0.6 | 270° | floor | 1 шт. 2048→1024 | 0.33 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (60 см); высота 28 см  в ОС 60 см |
| `tool_saw_nozhovka_idle` | `tool_saw_nozhovka.glb` | 49 280 → 2 940 (3 000) | 50 × 4 × 18 | 50 × 12 | ×0.5 | 270° | floor | 1 шт. 2048→512 | 0.16 | ⚠ подогнано по ширине; высота 18 см  в ОС 12 см |
| `tool_screwdriver_krestovaya_idle` | `tool_screwdriver_krestovaya.glb` | 49 594 → 2 940 (3 000) | 20 × 4 × 4 | 20 × 4 | ×0.2 | 270° | floor | 1 шт. 2048→512 | 0.14 | — |
| `tool_shovel_shtykovaya_idle` | `tool_shovel_shtykovaya.glb` | 48 634 → 7 840 (8 000) | 43 × 118 × 110 | 30 × 110 | ×1.18 | 270° | floor | 1 шт. 2048→1024 | 0.33 | ⚠ ширина 43 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `tool_sledge_malaya_idle` | `tool_sledge_malaya.glb` | 48 318 → 7 840 (8 000) | 42 × 57 × 90 | 30 × 90 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.29 | ⚠ ширина 42 см  в ОС 30 см (> 15 %) — записано в DEVIATIONS.md |
| `tool_soldering_setevoy_idle` | `tool_soldering_setevoy.glb` | 46 724 → 2 940 (3 000) | 25 × 14 × 17 | 25 × 5 | ×0.25 | 270° | floor | 1 шт. 2048→512 | 0.17 | ⚠ подогнано по ширине; высота 17 см  в ОС 5 см |
| `tool_wrench_razvodnoy_idle` | `tool_wrench_razvodnoy.glb` | 46 920 → 2 940 (3 000) | 30 × 11 × 3 | 30 × 8 | ×0.3 | 270° | floor | 1 шт. 2048→512 | 0.16 | ⚠ подогнано по ширине; высота 3 см  в ОС 8 см |
| `toolbox_plastikovyy_idle` | `toolbox_plastikovyy.glb` | 43 974 → 2 940 (3 000) | 31 × 24 × 25 | 40 × 25 | ×0.314 | 270° | floor | 1 шт. 2048→512 | 0.19 | ⚠ ширина 31 см  в ОС 40 см (> 15 %) — записано в DEVIATIONS.md |
| `trade_stall_prilavok_idle` | `trade_stall_prilavok.glb` | 46 447 → 7 839 (8 000) | 98 × 58 × 110 | 160 × 110 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ ширина 98 см  в ОС 160 см (> 15 %) — записано в DEVIATIONS.md |
| `trader_npc_brodyachiy_idle` | `trader_npc_brodyachiy.glb` | 48 654 → 14 700 (15 000) | 139 × 99 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.79 | ⚠ ширина 139 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `trap_bear_kapkan_idle` | `trap_bear_kapkan.glb` | 47 664 → 2 940 (3 000) | 40 × 50 × 41 | 40 × 10 | ×0.501 | 0° | floor | 1 шт. 2048→512 | 0.20 | ⚠ подогнано по ширине; высота 41 см  в ОС 10 см |
| `treadmill_generator_begovaya_dorozhka_idle` | `treadmill_generator_begovaya_dorozhka.glb` | 46 021 → 14 699 (15 000) | 219 × 119 × 120 | 160 × 120 | ×2.19 | 270° | floor | 1 шт. 2048→1024 | 0.59 | ⚠ ширина 219 см  в ОС 160 см (> 15 %) — записано в DEVIATIONS.md |
| `van_idle` | `van.glb` | 44 804 → 7 840 (8 000) | 500 × 276 × 261 | 500 × 150 | ×5 | 270° | floor | 1 шт. 2048→1024 | 0.44 | ⚠ подогнано по ширине; высота 261 см  в ОС 150 см |
| `veg_potato_kartofel_idle` | `veg_potato_kartofel.glb` | 48 550 → 2 940 (3 000) | 8 × 7 × 4 | 8 × 8 | ×0.08 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (8 см); высота 4 см  в ОС 8 см |
| `vest_armor_samodelnyy_idle` | `vest_armor_samodelnyy.glb` | 46 251 → 7 839 (8 000) | 46 × 39 × 60 | 45 × 60 | ×0.6 | 270° | floor | 1 шт. 2048→1024 | 0.48 | — |
| `wardrobe_derevyannyy_dvustvorchatyy_idle` | `wardrobe_derevyannyy_dvustvorchatyy.glb` | 45 388 → 14 700 (15 000) | 113 × 85 × 200 | 100 × 200 | ×2 | 270° | floor | 1 шт. 2048→1024 | 0.55 | — |
| `warehouse_idle` | `warehouse.glb` | 40 572 → 14 700 (15 000) | 1400 × 834 × 373 | 1400 × 600 | ×14 | 270° | floor | 1 шт. 2048→1024 | 0.72 | ⚠ подогнано по ширине; высота 373 см  в ОС 600 см |
| `watchtower_derevyannaya_idle` | `watchtower_derevyannaya.glb` | 45 473 → 14 699 (15 000) | 193 × 204 × 500 | 200 × 500 | ×5 | 270° | floor | 1 шт. 2048→1024 | 0.73 | — |
| `water_pump_ruchnoy_rychazhnyy_idle` | `water_pump_ruchnoy_rychazhnyy.glb` | 47 670 → 7 840 (8 000) | 36 × 28 × 60 | 50 × 60 | ×0.6 | 270° | floor | 1 шт. 2048→1024 | 0.34 | ⚠ ширина 36 см  в ОС 50 см (> 15 %) — записано в DEVIATIONS.md |
| `water_purifier_keramicheskiy_filtr_idle` | `water_purifier_keramicheskiy_filtr.glb` | 47 800 → 14 700 (15 000) | 43 × 59 × 100 | 60 × 100 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.51 | ⚠ ширина 43 см  в ОС 60 см (> 15 %) — записано в DEVIATIONS.md |
| `water_tablets_hlornye_idle` | `water_tablets_hlornye.glb` | 47 757 → 2 939 (3 000) | 10 × 4 × 3 | 6 × 10 | ×0.1 | 270° | floor | 1 шт. 2048→512 | 0.14 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (10 см); высота 3 см  в ОС 10 см |
| `water_tower_kirpichnaya_idle` | `water_tower_kirpichnaya.glb` | 45 868 → 14 700 (15 000) | 424 × 374 × 1000 | 400 × 1000 | ×10 | 270° | floor | 1 шт. 2048→1024 | 0.63 | — |
| `weapon_bat_derevyannaya_idle` | `weapon_bat_derevyannaya.glb` | 47 010 → 7 838 (8 000) | 90 × 14 × 14 | 90 × 10 | ×0.9 | 270° | floor | 1 шт. 2048→1024 | 0.28 | ⚠ подогнано по ширине; высота 14 см  в ОС 10 см |
| `weapon_bow_ohotnichiy_idle` | `weapon_bow_ohotnichiy.glb` | 48 382 → 7 840 (8 000) | 110 × 104 × 33 | 70 × 110 | ×1.1 | 270° | floor | 1 шт. 2048→1024 | 0.39 | ⚠ лежит плашмя / свёрнуто — подогнано по длинной стороне (110 см); высота 33 см  в ОС 110 см |
| `weapon_machete_machete_idle` | `weapon_machete_machete.glb` | 48 314 → 7 840 (8 000) | 70 × 7 × 33 | 70 × 8 | ×0.7 | 270° | floor | 1 шт. 2048→1024 | 0.32 | ⚠ подогнано по ширине; высота 33 см  в ОС 8 см |
| `weapon_pipe_stalnaya_truba_idle` | `weapon_pipe_stalnaya_truba.glb` | 48 364 → 7 840 (8 000) | 80 × 17 × 28 | 80 × 8 | ×0.8 | 270° | floor | 1 шт. 2048→1024 | 0.34 | ⚠ подогнано по ширине; высота 28 см  в ОС 8 см |
| `weapon_pistol_9_mm_idle` | `weapon_pistol_9_mm.glb` | 46 228 → 2 940 (3 000) | 19 × 4 × 14 | 20 × 14 | ×0.19 | 270° | floor | 1 шт. 2048→512 | 0.20 | — |
| `weapon_shotgun_pompovyy_idle` | `weapon_shotgun_pompovyy.glb` | 47 442 → 7 840 (8 000) | 100 × 7 × 20 | 100 × 15 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.31 | ⚠ подогнано по ширине; высота 20 см  в ОС 15 см |
| `well_hand_ruchnoy_kolodets_s_vorotom_idle` | `well_hand_ruchnoy_kolodets_s_vorotom.glb` | 47 642 → 7 839 (8 000) | 106 × 84 × 130 | 90 × 130 | ×1.3 | 270° | floor | 1 шт. 2048→1024 | 0.46 | ⚠ ширина 106 см  в ОС 90 см (> 15 %) — записано в DEVIATIONS.md |
| `wind_turbine_malyy_gorizontalnyy_idle` | `wind_turbine_malyy_gorizontalnyy.glb` | 48 394 → 14 699 (15 000) | 186 × 145 × 300 | 100 × 300 | ×3 | 270° | floor | 1 шт. 2048→1024 | 0.50 | ⚠ ширина 186 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `window_basic_tseloe_idle` | `window_basic_tseloe.glb` | 44 600 → 14 698 (15 000) | 55 × 20 × 100 | 100 × 100 | ×1 | 270° | floor | 1 шт. 2048→1024 | 0.49 | ⚠ ширина 55 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `workbench_basic_derevyannyy_bazovyy_idle` | `workbench_basic_derevyannyy_bazovyy.glb` | 40 080 → 7 840 (8 000) | 160 × 82 × 101 | 160 × 95 | ×1.6 | 0° | floor | 1 шт. 2048→1024 | 0.44 | — |
| `workbench_electronics_nastolnyy_idle` | `workbench_electronics_nastolnyy.glb` | 43 041 → 7 839 (8 000) | 140 × 72 × 120 | 140 × 95 | ×1.4 | 0° | floor | 1 шт. 2048→1024 | 0.64 | ⚠ подогнано по ширине; высота 120 см  в ОС 95 см |
| `zombie_brute_zdorovyak_idle` | `zombie_brute_zdorovyak.glb` | 49 594 → 14 700 (15 000) | 213 × 68 × 200 | 120 × 200 | ×2.13 | 270° | floor | 1 шт. 2048→1024 | 0.47 | ⚠ ширина 213 см  в ОС 120 см (> 15 %) — записано в DEVIATIONS.md |
| `zombie_runner_begun_idle` | `zombie_runner_begun.glb` | 47 888 → 14 700 (15 000) | 71 × 28 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.56 | ⚠ ширина 71 см  в ОС 100 см (> 15 %) — записано в DEVIATIONS.md |
| `zombie_walker_hodyachiy_idle` | `zombie_walker_hodyachiy.glb` | 47 928 → 14 700 (15 000) | 91 × 39 × 180 | 100 × 180 | ×1.8 | 270° | floor | 1 шт. 2048→1024 | 0.56 | — |


## Партия 2026-10-11/12 (Google Диск, 202 файла с именами Tripo)

Опознано по снимкам с 4 сторон и названо по `docs/TRIPO_BUILDINGS.md` — **202 из 202**, обработано все. Настройки
(название, размер, крепление, лимит) — `tripo/extra.json`, повороты — `tripo/rotate.json`. Вторые варианты одной вещи —
с суффиксом `_b`, `_c`, `_d`, `_e` (игра может брать любой). Листы — `renders/_review/tripo_2026-10-12_*.jpg`
(дома, улица, машины, отделка, блоки, шахта, тюрьма, буквы и двери). После обработки — `tools/glb_clean.py`
(ошмётки убраны у 2 моделей).

**Размеры:** дома — по ширине из запроса (8–24 м), высота по пропорциям; отделка и стены шахты/тюрьмы — ровно 1 × 1 м,
толщина 10 см; блоки — ровно 1 × 1 × 1 м; буквы — высота 1 м (все знаки в одном масштабе); двери — 2,1 м каждая;
машины — длина: седан 4,5 м, хэтчбек 4 м, универсал/полиция 4,8 м, пикап 5,2 м, фургон 5 м, автодом 7 м,
автобус 11 м, мотоцикл 2,1 м, велосипед 1,8 м. Лимит: дома, кран, ангары, ТЦ, вышки — 15 000.

**Разрезано:** `letters_a_j` → `letter_a…f, h, i, j` (**G нет** — Tripo пропустил); вторая модель букв → `letter_l, m, o, p, q, r, s`
(это не K–T: **нет K, N, T**); `letters_u_z_0_3` → `letter_u, v, w, x`, `digit_0…3` (**нет Y, Z**);
`digits_4_9_signs` → `digit_4…9`, `sign_amp`, `sign_excl`, `sign_dash`; два набора дверей → `door_1…6` и `door_7…11`.

**Персонажей с ригом в этой партии нет** (нет файлов из `TRIPO_CHARACTERS.md`) — скрипт для них готов: `tools/char_process.py`
(скелет и анимации сохраняет, рост 1,8 м, поворот, облегчение).

**Новое, чего нет в списках (дал понятные имена):** `block_concrete_cracked`, `block_dirt_cracked`, `block_soil_layers`, `block_soil_layers_b`, `building_ruin_1`, `building_ruin_2`, `car_old_blue`, `crates_stack`, `finish_pegboard`, `finish_plaster_window`, `house_cottage`, `house_porch`, `house_townhouse`, `house_two_story`, `house_two_story_b`, `house_wood_b`, `house_wood_c`, `house_wood_d`, `letters_partial_l_s`, `mine_cart_wood`, `mine_wall_planks_stone`, `mine_wall_planks_stone_b`, `prison_wall_mesh`, `ruin_column`, `ruin_pipe_wall`, `shack_brick`, `shack_wood`, `shop_cafe_bld`, `shop_general`, `tent_camp_aframe`.

**Не удалось / проверить:**
- `mine_wall_mesh` — облегчилась только до 16 090 треугольников (сетка-решётка, лимит 8 000);
- `decor_` и `house_*`: где Tripo сделал дом другой формы, высота может отличаться от ожидаемой — смотреть в игре;
- `car_tarp_b` — машина под брезентом (голубой), `car_old_blue` — старая машина без брезента;
- `prison_armory_cage` — «здание-клетка», а не клетка в комнату.

**Чего нет по списку TRIPO_BUILDINGS (121):**
- отделка (1–24): 1 `finish_concrete_ok`, 2 `finish_concrete_damaged`, 3 `finish_concrete_ruined`, 4 `finish_plaster_ok`, 6 `finish_plaster_ruined`, 10 `finish_wood_panels_ok`, 12 `finish_wood_panels_ruined`, 13 `finish_tiles_ok`, 15 `finish_tiles_ruined`, 18 `finish_metal_ruined`, 19 `finish_brick_ok`, 21 `finish_brick_ruined`, 22 `finish_bunker_ok`, 23 `finish_bunker_damaged`, 24 `finish_bunker_ruined`;
- фасады (25–45): 25 `facade_brick_window_ok`, 26 `facade_brick_window_damaged`, 27 `facade_brick_window_ruined`, 28 `facade_brick_door_ok`, 29 `facade_brick_door_damaged`, 30 `facade_brick_door_ruined`, 31 `facade_plaster_window_ok`, 32 `facade_plaster_window_damaged`, 33 `facade_plaster_window_ruined`, 34 `facade_wood_window_ok`, 35 `facade_wood_window_damaged`, 36 `facade_wood_window_ruined`, 37 `facade_concrete_window_ok`, 38 `facade_concrete_window_damaged`, 39 `facade_concrete_window_ruined`, 40 `facade_garage_ok`, 42 `facade_garage_ruined`, 43 `facade_blank_ok`, 44 `facade_blank_damaged`, 45 `facade_blank_ruined`;
- крыши (46–63): 46 `roof_gable_tiles_ok`, 47 `roof_gable_tiles_damaged`, 48 `roof_gable_tiles_ruined`, 49 `roof_gable_metal_ok`, 50 `roof_gable_metal_damaged`, 51 `roof_gable_metal_ruined`, 52 `roof_flat_ok`, 53 `roof_flat_damaged`, 54 `roof_flat_ruined`, 55 `roof_chimney_ok`, 56 `roof_chimney_damaged`, 57 `roof_chimney_ruined`, 58 `roof_attic_window_ok`, 59 `roof_attic_window_damaged`, 60 `roof_attic_window_ruined`, 61 `roof_antenna_ok`, 62 `roof_antenna_damaged`, 63 `roof_antenna_ruined`;
- витрины (64–84): 64 `shop_grocery_ok`, 65 `shop_grocery_damaged`, 66 `shop_grocery_ruined`, 67 `shop_pharmacy_ok`, 68 `shop_pharmacy_damaged`, 69 `shop_pharmacy_ruined`, 70 `shop_guns_ok`, 71 `shop_guns_damaged`, 72 `shop_guns_ruined`, 73 `shop_hardware_ok`, 74 `shop_hardware_damaged`, 75 `shop_hardware_ruined`, 76 `shop_cafe_ok`, 77 `shop_cafe_damaged`, 78 `shop_cafe_ruined`, 79 `shop_clothes_ok`, 80 `shop_clothes_damaged`, 81 `shop_clothes_ruined`, 82 `shop_gas_ok`, 83 `shop_gas_damaged`, 84 `shop_gas_ruined`;
- разрушения и декор (85–112): 85 `ruin_wall_hole`, 86 `ruin_wall_cracks`, 87 `ruin_ceiling_collapse`, 88 `ruin_rubble_pile`, 89 `ruin_rubble_small`, 90 `ruin_floor_broken`, 91 `ruin_beam_fallen`, 92 `ruin_burnt_wall`, 94 `ruin_wires`, 95 `wall_photos`, 96 `wall_mirror`, 97 `wall_hooks_coats`, 98 `wall_calendar`, 99 `wall_tv`, 100 `wall_fan`, 101 `wall_trophy`, 102 `wall_dartboard`, 103 `wall_window_boarded`, 104 `wall_graffiti`, 105 `ext_balcony`, 106 `ext_fire_escape`, 108 `ext_awning`, 109 `ext_ac_unit`, 110 `ext_mailbox`, 111 `ext_billboard`;
- дома (113–147): 121 `shop_guns_bld`, 132 `cemetery`, 133 `pool`, 142 `pet_shop`;
- улица (148–165): 161 `storage_tank`, 163 `scaffold_platform`;
- буквы (166–169): 167 `letters_k_t` (частично сделаны — см. выше);
- шахта (170–197): 170 `mine_elevator_cage`, 171 `mine_elevator_shaft`, 172 `mine_winch`, 174 `mine_support_steel`, 175 `mine_beam_wood`, 176 `mine_beam_steel`, 189 `mine_rails_curve`, 194 `mine_barrel`;
- тюрьма (198–211): 198 `prison`, 206 `prison_table_interrogation`;
- блоки (212–226): 213 `block_asphalt`, 218 `block_rubble`, 220 `block_coal`, 221 `block_ore_iron`, 223 `block_wood`;
- транспорт (227–236): .

---

## Партия 2026-10-12 (папка Диска `1D7CH7QzUHZcksZhnjqzayPpK5oXB5T6v`) — новые 167 моделей

**Что было в папке:** 411 файлов. 257 — **байт в байт старые** (уже обработаны раньше), 24 — повторные копии одного файла,
**146 новых**. Новые опознаны по виду (4 стороны), имена — по `docs/TRIPO_BATCH_2026-10-12.md` и `docs/TRIPO_CHARACTERS.md`.
Из 146 файлов получилось **167 моделей**: 132 обычных + 5 со скелетом + 30 кусков из 9 наборов.

**Листы превью:** `renders/_review/tripo_2026-10-12_b3_character.jpg` (74 человека), `…_creature.jpg` (18 животных),
`…_clothing.jpg` (19 вещей на человека), `…_item.jpg` (12), `…_decor_set.jpg` (9), `…_sets.jpg` (30 кусков наборов),
`…_rigged.jpg` (5 со скелетом).

**Со скелетом (риг Mixamo, анимации внутри) — `tools/char_process.py`:** `char_f_hoodie` (3 анимации),
`body_f_rig` (76), `body_m_rig` (93), `body_m_rig_b` (31), `body_m_rig_c` (0). Рост 1,68 / 1,8 м, лицом к −Y.
⚠ `body_f_rig` 8,5 МБ, `body_m_rig` 10,5 МБ, `body_m_rig_b` 4,5 МБ — больше 3 МБ из-за анимаций (сетка и текстуры лёгкие).
**Остальные 71 человек — без скелета** (статичные): для анимаций нужен риг в Tripo («Гуманоид», Mixamo).
Исправлено: `char_process.py` мерил и выгружал вместе с телом служебный шар показа костей — люди выходили вдвое меньше.

**Разрезано (`tools/split_parts.py`, новые режимы `--box` — вещи друг над другом, `--k` — касаются друг друга):**
3 кролика → `rabbit_hare`, `rabbit_white`, `rabbit_grey`; 6 птиц → `crow`, `pigeon`, `seagull`, `vulture`, `owl`, `duck`;
`set_gr_1` → `hat_gr_net`, `hat_gr_boonie`, `hat_gr_beret`; № 199 → `wrist_rope`, `wrist_shackles`, `back_yoke_buckets`;
`set_fm_2` → `hat_fm_wide`, `back_fm_rope`, `belt_fm_lantern`; Rust Dogs → `goggles_rd`, `back_rd_tire`, `back_rd_tank`;
№ 197 → `back_sack_ore`, `back_basket_coal`, `back_firewood`; № 201 → `tool_sledgehammer`, `tool_broom_push`,
`item_mop_bucket`; трубы → `joint_pipes_T`, `joint_pipes_X`, `pipes_end_caps`.

**Точка опоры вещей на человека:** шапки, капюшоны, противогаз, маски-шлемы — низ по центру; рюкзаки (`back_…`),
`goggles_rd`, `mask_ws_cloth` — центр задней стороны (+Y, сторона к телу).

**Отличия от списка `TRIPO_BATCH_2026-10-12.md`:**
- `dog_feral` занят в плане ОС (`dog_feral_odinochnaya`) — новая тощая собака названа `dog_thin`; ротвейлер — `dog_rottweiler` (в списке нет).
- Шахтёров (`char_miner_…`) в папке не нашёл. Наборы `set_fm_1`, `set_gr_2`, `set_s9_1`, `set_s9_2` целиком не пришли —
  поодиночке пришли только `hat_fm_hood`, `mask_gr_gas`, `hat_s9_hood`, `back_s9_air`. Не пришли № 198, 200, 202,
  `joint_pipes_set_1/2`, `joint_duct_set(_b)`, `joint_misc_set(_b)`, `rat_big`, `rat_mutant`, `char_free_f_nurse`.
- Уголки труб (`joint_pipes_T/X`, `pipes_end_caps`) и короба (`decor_duct_cross`, `decor_duct_straight`) — **сечение с прямыми
  кусками не подогнано** (точку опоры и масштаб по `decor_pipes_colored_h` нужно сделать отдельно); набор труб — Т, крест,
  заглушки (а не L, T, X, как в списке).
- Люди не из списков (дал понятные имена): `char_f_police(_b)`, `char_m_police`, `char_f_firefighter`, `char_m_firefighter`,
  `char_m_chef`, `char_f_old`, `char_m_adventurer`, `char_m_tactical`, `char_rd_raider`, `char_m_old_c`, военные
  `char_f_military(_b)`, `char_m_military(_b)`; тела без рига `body_base_female_b/c`, `body_base_male`; одежда для тела
  `top_hoodie_f/m`, `bottom_jeans_f/m`, `shoes_sneakers`.

**Проверить:** `hat_fm_hood` — 4 083 треугольника (лимит мелкого 3 000, сетка капюшона не облегчается без дыр);
`item_radio_vintage` — 7 840 (при 3 000 развалился, поставлен лимит 8 000).

| Имя | Что это | Файл на Диске | Размер, см | Треуг. | Поворот |
|---|---|---|---|---|---|
| body_base_female_b | Базовое тело — женщина, вариант (без рига) | 3D-модель женского персонажа | 161×33×168 | 14700 | 270° |
| body_base_female_c | Базовое тело — женщина, вариант 2 (без рига) | stylized female 3d model | 166×31×168 | 14700 | 0° |
| body_base_male | Базовое тело — мужчина (без рига) | низкополигональная 3D-модель человека | 180×34×180 | 14700 | 270° |
| char_f_doctor | №5 Врач | doctor 3d model | 145×32×168 | 14698 | 270° |
| char_f_firefighter | Пожарная | firefighter 3d model (1) | 171×45×170 | 14700 | 270° |
| char_f_mechanic | №3 Механик, хвост | 3d character model (2) | 149×38×168 | 14700 | 270° |
| char_f_military | №4 Военная (комбинезон) | 3D-модель военного комбинезона | 141×30×168 | 14700 | 270° |
| char_f_military_b | №4 Военная (вариант, капюшон) | 3D-модель военного персонажа | 69×39×168 | 14700 | 270° |
| char_f_old | Старушка | elderly woman 3d model | 140×43×162 | 14700 | 270° |
| char_f_police | Полицейская | police officer 3d model (1) | 154×35×170 | 14700 | 270° |
| char_f_police_b | Полицейская (вариант) | police officer 3d model | 159×34×170 | 14700 | 270° |
| char_fm_f | №129 Ferrymen — женщина | stylized character 3d model (4) | 146×50×168 | 14700 | 270° |
| char_fm_f_thin | №133 Ferrymen — худая дозорная | tattered cloak character 3d model | 148×42×166 | 14700 | 270° |
| char_fm_leader | №131 Ferrymen — Martha «Ledger» | witch 3d model | 152×51×170 | 14700 | 270° |
| char_fm_m | №130 Ferrymen — мужчина | rugged adventurer 3d model | 155×44×180 | 14700 | 270° |
| char_fm_m_big | №132 Ferrymen — гребец-здоровяк | strongman 3d model | 175×81×190 | 14700 | 270° |
| char_fm_m_young | №134 Ferrymen — молодой перевозчик | torn shirt prisoner 3d model | 157×32×176 | 14700 | 270° |
| char_free_f_denim | №7 Спорт | stylized character 3d model (2) | 146×29×168 | 14700 | 270° |
| char_free_f_rain | Девушка в жёлтом дождевике | stylized character 3d model (1) | 146×36×165 | 14700 | 270° |
| char_free_m_hermit | №27 Старик (вариант, длинные волосы) | elderly man 3d model (1) | 170×50×175 | 14700 | 270° |
| char_free_m_hunter | №21 Лесоруб | stylized outdoorsman 3d model | 188×41×182 | 14700 | 270° |
| char_free_m_office | Мужчина в рваном костюме | tattered suit character 3d model | 155×33×176 | 14700 | 270° |
| char_free_m_teacher | №27 Старик | elderly man 3d model | 158×31×175 | 14700 | 270° |
| char_gr_f | №141 Garrison — женщина | soldier 3d model | 152×31×170 | 14700 | 270° |
| char_gr_f_short | №145 Garrison — санитарка | military medic 3d model | 164×44×168 | 14700 | 270° |
| char_gr_leader | №143 Garrison — Major Ian Rowan | military officer 3d model | 171×37×182 | 14700 | 270° |
| char_gr_m | №142 Garrison — мужчина | military soldier 3d model (2) | 167×40×180 | 14700 | 270° |
| char_gr_m_big | №144 Garrison — пулемётчик | military soldier 3d model | 171×61×188 | 14700 | 270° |
| char_gr_m_old | №146 Garrison — связист постарше | military soldier 3d model (1) | 165×35×178 | 14700 | 270° |
| char_iw_f | №105 Iron Wheel — женщина | folk dancer 3d model | 141×45×168 | 14700 | 270° |
| char_iw_f_tall | №108 Iron Wheel — высокая с дредами | stylized character 3d model (3) | 150×39×180 | 14700 | 270° |
| char_iw_leader | №107 Iron Wheel — Silas «Limp» | patchwork coat character 3d model | 161×36×178 | 14698 | 270° |
| char_iw_m | №106 Iron Wheel — мужчина | poncho character 3d model | 157×53×178 | 14700 | 270° |
| char_iw_m_old | №109 Iron Wheel — старый торговец | old man 3d model (2) | 188×64×172 | 14700 | 270° |
| char_iw_m_young | №110 Iron Wheel — молодой погонщик | low-poly character 3d model (1) | 154×41×176 | 14700 | 270° |
| char_m_adventurer | Путник с большим рюкзаком | 3D-модель искателя приключений с рюкзаком | 163×81×180 | 14700 | 270° |
| char_m_chef | Повар | chef character 3d model | 187×64×180 | 14699 | 270° |
| char_m_firefighter | Пожарный | firefighter 3d model | 160×31×180 | 14700 | 270° |
| char_m_hoodie | №22 Худи (капюшон) | стилизованная 3D-модель персонажа в капюшоне | 166×37×180 | 14700 | 270° |
| char_m_military | №20 Военный | 3D-модель военного солдата | 90×35×180 | 14700 | 270° |
| char_m_military_b | №20 Военный (вариант) | 3D-модель военного солдата (1) | 170×33×178 | 14698 | 270° |
| char_m_old_c | №27 Старик (вариант, куртка) | old man 3d model (1) | 184×49×172 | 14700 | 270° |
| char_m_police | №25 Полицейский | police officer 3d model (2) | 162×38×180 | 14698 | 270° |
| char_m_tactical | Мужчина в тактическом костюме с капюшоном | тактический костюм с капюшоном, 3D-модель | 85×35×180 | 14700 | 270° |
| char_m_worker | №23 Рабочий | muscular worker 3d model | 164×64×185 | 14700 | 270° |
| char_prisoner_f | Заключённая | prisoner 3d model (2) | 150×39×168 | 14700 | 270° |
| char_prisoner_m | Заключённый | prisoner 3d model (1) | 175×36×180 | 14700 | 270° |
| char_prisoner_m_old | Заключённый (полосатая роба) | prisoner 3d model | 166×34×178 | 14700 | 270° |
| char_rd_f | №117 Rust Dogs — женщина | barbarian warrior 3d model (1) | 156×44×170 | 14700 | 270° |
| char_rd_f_b | №117 Rust Dogs — женщина (вариант) | stylized female character 3d model | 149×32×170 | 14700 | 270° |
| char_rd_f_big | №121 Rust Dogs — крепкая рейдерша | tribal warrior 3d model | 184×51×175 | 14700 | 270° |
| char_rd_leader | №119 Rust Dogs — Gus Brody «Brute» | rusty battle armor 3d model | 167×76×195 | 14699 | 270° |
| char_rd_m | №118 Rust Dogs — мужчина | post-apocalyptic fighter 3d model | 161×39×180 | 14700 | 270° |
| char_rd_m_old | №122 Rust Dogs — старый одноглазый | post-apocalyptic character 3d model | 151×57×185 | 14700 | 270° |
| char_rd_m_thin | №120 Rust Dogs — тощий псих | stylized zombie 3d model | 163×33×176 | 14700 | 270° |
| char_rd_raider | Rust Dogs — рейдер в маске | фэнтезийный разбойник 3D-модель | 177×45×182 | 14700 | 270° |
| char_s9_f | №153 Site-9 — женщина | stylized scientist 3d model | 151×38×168 | 14700 | 270° |
| char_s9_leader | №155 Site-9 — директор | lab coat scientist 3d model | 161×38×178 | 14700 | 270° |
| char_s9_m | №154 Site-9 — мужчина (жёлтый костюм) | low-poly character 3d model | 164×47×180 | 14700 | 270° |
| char_s9_m_guard | №156 Site-9 — охранник | stylized armored figure 3d model | 114×41×182 | 14700 | 270° |
| char_s9_m_subject | №158 Site-9 — подопытный | low poly human 3d model | 160×36×178 | 14700 | 270° |
| char_slave_f | Девушка в лохмотьях | ragged girl 3d model | 59×38×165 | 14700 | 270° |
| char_slave_m | Узник в лохмотьях | ragged prisoner 3d model | 171×33×176 | 14700 | 270° |
| char_slave_m_old | №27 Старик (вариант, свитер) | old man 3d model | 174×41×174 | 14700 | 270° |
| char_ws_f | №93 Wellspring — женщина | stylized 3d character | 149×40×168 | 14700 | 270° |
| char_ws_f_round | №97 Wellspring — полная девушка в дождевике | stylized human 3d model (1) | 163×52×162 | 14700 | 270° |
| char_ws_leader | №95 Wellspring — Anna Weller | stylized character 3d model | 150×31×170 | 14700 | 270° |
| char_ws_m | №94 Wellspring — мужчина | stylized human 3d model | 164×37×178 | 14700 | 270° |
| char_ws_m_old | №96 Wellspring — старик-огородник | elderly man 3d model (2) | 169×37×174 | 14700 | 270° |
| zombie_fat | №39 Зомби — громила | zombie 3d model | 193×79×190 | 14699 | 270° |
| zombie_firefighter | Зомби-пожарный | zombie firefighter 3d model | 159×35×178 | 14700 | 270° |
| zombie_hospital | №18 Зомби — женщина | zombie 3d model (1) | 148×34×168 | 14700 | 270° |
| zombie_office | №38 Зомби — мужчина | 3D-модель персонажа зомби | 144×41×175 | 14700 | 270° |
| zombie_runner | №18 Зомби — женщина (вариант) | zombie character 3d model | 145×33×168 | 14699 | 270° |
| back_iw_pack | №115 Огромный рюкзак торговца | adventure backpack 3d model (1) | 65×54×90 | 7840 | 270° |
| back_s9_air | №163 Баллон с воздухом на спину | lab equipment 3d model | 58×62×60 | 7838 | 270° |
| back_ws_basket | №103 Плетёная корзина-рюкзак | woven basket 3d model | 49×65×60 | 7839 | 270° |
| bottom_jeans_f | Джинсы женские (одежда для тела) | 3D-модель женский-джинсов | 40×29×100 | 7840 | 270° |
| bottom_jeans_m | Джинсы мужские (одежда для тела) | 3D-модель синих мужский джинсов | 46×35×105 | 7838 | 270° |
| hat_bandana | №44 Бандана | bandana 3d model (1) | 23×15×30 | 2940 | 270° |
| hat_fm_hood | №136 Капюшон из сети и тряпья | hooded mask 3d model | 40×33×45 | 4083 | 270° |
| hat_iw_feather | №111 Широкая шляпа с перьями | low-poly hat 3d model | 48×48×30 | 2940 | 270° |
| hat_s9_hood | №160 Капюшон защитного костюма | hazmat helmet 3d model | 37×36×45 | 2940 | 270° |
| hat_ws_beanie | №100 Вязаная шапка с помпоном | beanie hat 3d model | 24×24×28 | 2940 | 270° |
| hat_ws_bucket | №104 Панама | low-poly bucket hat 3d model | 32×32×17 | 2940 | 270° |
| hat_ws_straw | №99 Соломенная шляпа | straw hat 3d model | 45×45×17 | 2940 | 270° |
| mask_gr_gas | №152 Армейский противогаз с капюшоном | military gas mask 3d model | 32×35×42 | 2940 | 270° |
| mask_rd_scrap | №123 Маска из ржавого металла | rusted mask 3d model | 24×27×32 | 2939 | 270° |
| mask_rd_scrap_b | №123 Маска из ржавого металла (вариант) | stylized mask 3d model | 27×30×32 | 2940 | 270° |
| mask_ws_cloth | №102 Самодельная маска на лицо | stitch patch mask 3d model | 22×11×15 | 2939 | 270° |
| shoes_sneakers | Кроссовки (одежда для тела) | 3D-модель кроссовок | 26×19×8 | 2940 | 270° |
| top_hoodie_f | Худи женское (одежда для тела) | 3D-модель женской толстовки с капюшоном | 150×35×102 | 7840 | 270° |
| top_hoodie_m | Худи мужское (одежда для тела) | 3D-модель мужской толстовки с капюшоном | 160×39×105 | 7840 | 270° |
| bear_black | Медведь чёрный | low poly bear 3d model | 69×155×100 | 7838 | 0° |
| bear_brown | Медведь бурый | low poly bear 3d model (1) | 71×160×110 | 7840 | 0° |
| bear_mutant | Медведь-мутант | low-poly bear 3d model | 92×180×120 | 7840 | 0° |
| deer_red | №89 Олень (благородный) | low-poly deer 3d model | 103×185×200 | 7840 | 270° |
| deer_roe | №89 Олень (самка) | deer 3d model | 37×116×140 | 7840 | 180° |
| deer_white | №89 Олень (рога) | low poly deer 3d model | 78×149×180 | 7838 | 180° |
| dog_thin | №80 Дикая собака (тощая) | low-poly dog 3d model | 25×95×60 | 7840 | 0° |
| dog_husky | №91 Волк (светлый) | low poly wolf 3d model | 27×108×80 | 7840 | 0° |
| dog_raider | №80 Дикая собака (с ошейником) | low-poly dog 3d model (2) | 26×89×60 | 7838 | 0° |
| dog_rottweiler | Собака — ротвейлер | dog 3d model | 27×84×70 | 7840 | 0° |
| dog_shepherd | №81 Овчарка | low-poly dog 3d model (3) | 21×96×65 | 7840 | 0° |
| dog_terrier | Собака — терьер | low poly dog 3d model | 20×53×45 | 2939 | 0° |
| dog_zombie | №82 Собака-зомби | low-poly dog 3d model (1) | 26×105×65 | 7840 | 0° |
| moose_bull | Лось | moose 3d model | 117×222×230 | 7839 | 180° |
| moose_cow | Лосиха | low poly horse 3d model | 60×212×190 | 7840 | 180° |
| moose_mutant | Лось-мутант | fantasy creature 3d model | 123×226×240 | 7840 | 180° |
| rat_grey | №85 Крыса | low-poly rat 3d model | 7×24×8 | 2940 | 180° |
| wolf | №91 Волк | 3D-модель волка | 29×120×80 | 7840 | 270° |
| decor_barrel_rusty | Ржавая бочка | ржавая металлическая бочка, 3D-модель | 67×67×90 | 7840 | 270° |
| decor_dirt_mound | Холм земли | 3D-модель земляного холма | 150×144×49 | 7840 | 270° |
| decor_duct_cross | Короб вентиляции — крестовина | cross pipe connector 3d model | 150×161×66 | 7840 | 0° |
| decor_duct_straight | Короб вентиляции — прямой | industrial cuboid prop 3d model | 150×162×80 | 7840 | 0° |
| decor_sign_weathered | Старая доска объявлений | выветренная вывеска, 3D-модель | 117×37×180 | 14700 | 0° |
| log_pile | Поленница | 3D-модель деревянных бревен | 110×145×96 | 7839 | 270° |
| rug_bear_skin | Медвежья шкура | bear rug 3d model (1) | 200×142×48 | 7840 | 0° |
| rug_persian | Ковёр узорный | persian rug 3d model | 200×138×8 | 7840 | 0° |
| rug_round_braided | Круглый плетёный коврик | round braided rug 3d model | 120×114×12 | 7838 | 270° |
| item_brick_wrapped | Свёрток (обёрнутый кирпич) | 3D-модель обернутого кирпича | 30×22×12 | 2940 | 270° |
| item_food_foil | Еда в фольге | 3D-модель закуски в фольге | 25×13×6 | 2940 | 270° |
| item_map | №77 Карта | 3D-модель сложенной карты | 40×46×6 | 2940 | 270° |
| item_medkit | №78 Аптечка | 3D-модель аптечки первой помощи (2) | 16×8×22 | 2939 | 270° |
| item_medkit_b | №78 Аптечка (вариант) | 3D-модель аптечки первой помощи (3) | 16×8×22 | 2940 | 270° |
| item_pills | Флакон с таблетками | 3D-модель флакона с таблетками | 16×6×4 | 2940 | 270° |
| item_radio_vintage | Радиоприёмник старый | 3D-модель винтажного радиоприемника | 45×25×40 | 7840 | 270° |
| mat_bolts | Ржавые болты (кучка) | ржавые болты 3D-модель | 30×21×12 | 2940 | 270° |
| log_single | Бревно | 3D-модель деревянного бревна (1) | 100×36×34 | 7839 | 270° |
| planks_bundle | Доски связкой | 3D-модель деревянных досок | 150×37×11 | 7839 | 270° |
| pickaxe_alt | Кирка (вариант) | 3D-модель кирки | 90×66×18 | 7840 | 0° |
| wrench_alt | Гаечный ключ (вариант) | 3D-модель гаечного ключа | 9×8×30 | 2940 | 270° |

---

## Партия 2026-10-12 — доделано (уголки, тела со скелетом, капюшон)

### 1. Уголки и стыки — сечение как у прямых кусков (`tools/fit_joint.py`)

Скрипт меряет толщину пучка/короба по срезам **без хомутов и фланцев** (нижняя четверть толщин по срезам — хомут и
фланец толще) у прямого куска и у каждой ветки уголка и масштабирует уголок **по каждой оси отдельно**. Центр стыка — в
начале координат, ветки по X и Y (в игре), задняя сторона — у стены (z = 0, как у прямых кусков, модель — к зрителю).
Лист проверки: `renders/_review/tripo_2026-10-12_b3_joints.jpg` — каждый уголок с прямыми кусками, состыкованными по осям.

| Уголок | К чему подогнан | Ветки | Итог, см (Ш×Г×В в Blender) |
|---|---|---|---|
| `joint_pipes_T` | гориз. ветка = `decor_pipes_colored_h` (пучок 32,3 × глубина 16,9), верт. = ширине `_v` (42,6) | влево, вправо, вниз | 142 × 18 × 111 |
| `joint_pipes_X` | то же | влево, вправо, вверх, вниз | 152 × 27 × 120 |
| `pipes_end_caps` | `decor_pipes_colored_h` (длина — в масштабе высоты) | влево и вправо, закрыты | 128 × 25 × 48 |
| `joint_duct_X` (был `decor_duct_cross`) | `decor_metal_duct`: высота 41,1, глубина 45,9; верт. ветка — тот же короб, повёрнутый | 4 стороны | 123 × 47 × 121 |
| `joint_duct_T` (был `decor_duct_straight`) | то же | вверх, вниз, влево | 79 × 47 × 94 |

- **Цвета труб** — как надо: в горизонтали сверху вниз жёлтая, синяя, красная; в вертикали слева направо жёлтая, синяя,
  красная (`joint_pipes_T`, `joint_pipes_X`, `pipes_end_caps`). Не перекрашивал.
- ⚠ **Сами прямые трубы разной глубины:** `decor_pipes_colored_h` — пучок 16,9 см (3 ряда × 2 трубы в глубину),
  `decor_pipes_colored_v` — 34,1 см. У уголка одна глубина — подогнана под горизонтальный (16,9). Вертикальный прямой
  кусок у стыка толще уголка в глубину (на листе в 3/4 видно). Чтобы совпадало и тут — нужен `_v` той же глубины.
- ⚠ **Число труб в пучке у уголков другое** (у T и креста в ветке 2 × 2 трубы, у прямого 3 × 2) — Tripo нарисовал так;
  совпадает толщина пучка, отдельные трубы на стыке не продолжаются одна в одну.
- `decor_duct_straight` оказался **не прямым коробом, а T-стыком** (прямой проход + ветка вбок), лежал на полу и был
  повёрнут на 9,6° — поставлен в плоскость стены, выровнен по осям и назван `joint_duct_T`. Второго варианта прямого
  куска нет. Крест (`decor_duct_cross`) тоже лежал — поставлен, выровнен на 3,6°.
- ⚠ У `joint_duct_T` сверху (теперь — к зрителю) открытая дыра в середине: так сгенерировал Tripo. Фланцы у уголков —
  свои (в масштабе модели), с фланцами прямого короба по размеру не сверял.
- Наборы `joint_pipes_set_1/2` (L-уголки), `joint_duct_set(_b)`, `joint_misc_set(_b)` ещё не пришли.

### 2. Тела со скелетом — сетка отдельно, анимации отдельно (`tools/char_process.py`)

- `export/<имя>_idle.glb` — **сетка + скелет в позе покоя (T-поза), без анимаций**: 0,65–0,74 МБ.
- `export/anim/<имя>_anims.glb` — **скелет + все анимации, без сетки** (внутри крошечный невидимый треугольник на кости
  Hips: без привязанной сетки glTF пишет кости обычными узлами, а не скелетом — игра не узнала бы скелет).
- `export/anim/<имя>_info.json` — названия анимаций и костей.
- Исправлено попутно: убрана форма показа костей (Icosphere) — из-за неё люди были вдвое меньше.

**Кости — одинаковые (Mixamo):** 65 костей `mixamorig:…` у всех; у мужских тел (`body_m_rig`, `body_m_rig_b`) ещё служебная
`neutral_bone`; у `body_m_rig_c` нет 11 концевых костей (кончики пальцев `…4`, `HeadTop_End` — их анимации не двигают).
**Проверено:** анимация из файла женского тела надета на мужское (и наоборот, и на `body_m_rig_c`) — двигается правильно.
→ **Анимации подходят ко всем — это общий набор для всех людей.** Названия — запросы автора в Tripo (обрезаны Tripo до 64
знаков); по смыслу одинаковые повторяются в разных файлах.

| Файл | Анимаций | `_idle.glb` | `_anims.glb` |
|---|---|---|---|
| `body_m_rig` | 93 | 0.65 МБ | 9.89 МБ |
| `body_f_rig` | 76 | 0.74 МБ | 7.76 МБ |
| `body_m_rig_b` | 31 | 0.65 МБ | 3.85 МБ |
| `char_f_hoodie` | 3 | 0.71 МБ | 0.28 МБ |
| `body_m_rig_c` | 0 | 0.65 МБ | — |

В мужском и женском наборе общих названий: 74; всего разных: 96.

<details><summary><code>body_m_rig</code> — 93 анимаций</summary>

- Character bends down, picks up a small item from the floor with
- Character bends over an open box on the floor and searches thro
- Character chops a tree with an axe held in both hands, side swi
- Character climbs up a vertical ladder, hands and feet moving al
- Character crawls forward on the floor on hands and knees, slow 
- Character crouches and holds out food in one open hand toward a
- Character crouches in front of a door and picks a lock with two
- Character holding a gun takes out the empty magazine, inserts a
- Character holds a pistol in both hands at arm's length, aims fo
- Character holds a rifle at the shoulder, aims forward and fires
- Character kneels at a garden bed, makes a small hole in the soi
- Character kneels next to a body lying on the ground and searche
- Character kneels on the ground and butchers an animal carcass w
- Character lies on the back sleeping, chest slowly rising and fa
- Character makes a fast one-handed swing with a short melee weap
- Character quickly dodges to the side with a short step and lean
- Character reaches out, grabs a door handle, turns it and pulls 
- Character runs at a steady medium pace on a treadmill, arms swi
- Character sits and drives a car, both hands on the steering whe
- Character sits and eats from a bowl held in one hand, bringing 
- Character sits at a table and sews by hand, pulling a needle an
- Character sits down on the edge of a bed, then lies down on the
- Character sits holding an open book or note with both hands, re
- Character sits on a bicycle and pedals at a steady pace, hands 
- Character sits on a chair, back slightly leaning, hands resting
- Character sits on the ground and wraps a bandage around the own
- Character sits on the ground and wraps a bandage around the.001
- Character sits on the ground with legs crossed, leaning forward
- Character sneaks forward in a low crouch, slow careful steps, a
- Character standing raises a bottle to the mouth, tilts the head
- Character standing turns around 180 degrees on the spot with sm
- Character stands and bargains: holds out an item in one open ha
- Character stands and eats, holding a piece of food in one hand,
- Character stands at a control panel with a radio, presses butto
- Character stands at a stove and stirs food in a pot with a spoo
- Character stands at a table and repairs a device with a wrench 
- Character stands at a workbench and works with both hands: hamm
- Character stands bent forward with hands on the knees, breathin
- Character stands facing forward and talks, natural hand gesture
- Character stands holding a gun raised and aimed forward, steady
- Character stands holding the left forearm out in front of the c
- Character stands hunched, coughing hard, one hand over the mout
- Character stands in front of a tall cabinet, opens it and searc
- Character strikes the ground in front with a pickaxe held in bo
- Character swings a heavy two-handed weapon from over the should
- Character takes off a backpack from the shoulders, puts it on t
- Character walks forward carrying a heavy box in front of the ch
- Character walks forward limping on the right leg, putting littl
- Character walks slowly holding a flashlight in one hand at ches
- agree
- box_01
- box_02
- box_03
- chop
- climb
- defeat_03
- dig
- dive
- fall
- fire
- flee_01
- flee_02
- front_kick_01
- front_kick_02
- frustrated_01
- frustrated_02
- hit_to_body_01
- hit_to_body_02
- hit_to_head
- hit_to_side
- hit_to_stomach
- jump
- jump_down
- laugh_01
- lift_heavy
- look_around
- press-up
- run
- run_upstairs
- scratch
- shoot
- shovel
- sit
- slash
- swim
- wait
- walk
- выстрел с пистолета
- ложиться спать
- примает таблетки
- присел на одно колено, и смотрит в 
- стоит,  достает из кормана еду и сь
- что то мастерит за столом

</details>

<details><summary><code>body_f_rig</code> — 76 анимаций</summary>

- Character bends down, picks up a small item from the floor with
- Character bends over an open box on the floor and searches thro
- Character chops a tree with an axe held in both hands, side swi
- Character climbs up a vertical ladder, hands and feet moving al
- Character crawls forward on the floor on hands and knees, slow 
- Character crouches and holds out food in one open hand toward a
- Character crouches in front of a door and picks a lock with two
- Character holding a gun takes out the empty magazine, inserts a
- Character holds a pistol in both hands at arm's length, aims fo
- Character holds a rifle at the shoulder, aims forward and fires
- Character kneels at a garden bed, makes a small hole in the soi
- Character kneels next to a body lying on the ground and searche
- Character kneels on the ground and butchers an animal carcass w
- Character lies on the back sleeping, chest slowly rising and fa
- Character makes a fast one-handed swing with a short melee weap
- Character quickly dodges to the side with a short step and lean
- Character reaches out, grabs a door handle, turns it and pulls 
- Character runs at a steady medium pace on a treadmill, arms swi
- Character sits and drives a car, both hands on the steering whe
- Character sits and eats from a bowl held in one hand, bringing 
- Character sits at a table and sews by hand, pulling a needle an
- Character sits down on the edge of a bed, then lies down on the
- Character sits holding an open book or note with both hands, re
- Character sits on a bicycle and pedals at a steady pace, hands 
- Character sits on a chair, back slightly leaning, hands resting
- Character sits on the ground and wraps a bandage around the own
- Character sits on the ground and wraps a bandage around the.001
- Character sits on the ground with legs crossed, leaning forward
- Character sneaks forward in a low crouch, slow careful steps, a
- Character standing raises a bottle to the mouth, tilts the head
- Character standing turns around 180 degrees on the spot with sm
- Character stands and bargains: holds out an item in one open ha
- Character stands and eats, holding a piece of food in one hand,
- Character stands at a control panel with a radio, presses butto
- Character stands at a stove and stirs food in a pot with a spoo
- Character stands at a table and repairs a device with a wrench 
- Character stands at a workbench and works with both hands: hamm
- Character stands bent forward with hands on the knees, breathin
- Character stands facing forward and talks, natural hand gesture
- Character stands holding a gun raised and aimed forward, steady
- Character stands holding the left forearm out in front of the c
- Character stands hunched, coughing hard, one hand over the mout
- Character stands in front of a tall cabinet, opens it and searc
- Character strikes the ground in front with a pickaxe held in bo
- Character swings a heavy two-handed weapon from over the should
- Character takes off a backpack from the shoulders, puts it on t
- Character walks forward carrying a heavy box in front of the ch
- Character walks forward limping on the right leg, putting littl
- Character walks slowly holding a flashlight in one hand at ches
- box_01
- box_02
- box_03
- chop
- climb
- defeat_03
- flee_01
- flee_02
- front_kick_01
- front_kick_02
- frustrated_01
- frustrated_02
- hit_to_side
- jump
- laugh_01
- lift_heavy
- press-up
- scratch
- swim
- turn
- выстрел с пистолета
- ложиться спать
- примает таблетки
- присел на одно колено, и смотрит в 
- снимает с со спены рюкзак и смотри
- стоит,  достает из кормана еду и сь
- что то мастерит за столом

</details>

<details><summary><code>body_m_rig_b</code> — 31 анимаций</summary>

- agree
- box_01
- box_02
- box_03
- chop
- climb
- defeat_03
- dig
- dive
- fall
- fire
- front_kick_01
- front_kick_02
- hit_to_body_01
- hit_to_body_02
- hit_to_head
- hit_to_side
- hit_to_stomach
- jump_down
- lift_heavy
- look_around
- press-up
- run
- run_upstairs
- shoot
- shovel
- sit
- slash
- wait
- walk
- wave_goodbye_01

</details>

<details><summary><code>char_f_hoodie</code> — 3 анимаций</summary>

- climb
- front_kick_01
- front_kick_02

</details>

### 3. `hat_fm_hood` — не вышло

Сетка из тонких нитей: упрощение останавливается на ~4 000 треугольников. Пробовал: больше проходов, склейку швов,
растворение плоских мест, разрезку неправильных рёбер — лучший результат 3 748 без дыр, до 3 000 не опускается без
разрушения сетки. **Оставлен как был: 4 083 треугольника.**

### 4. Переименования автора

`dog_thin`, `log_single`, `log_pile`, `planks_bundle`, `pickaxe_alt`, `wrench_alt` — у себя переименовал и сырые файлы, и
превью, при пересборке старые имена не вернутся. Исходники коробов `decor_duct_cross/straight` убраны из
`tripo/extra.json` и `rotate.json` (готовые — `joint_duct_X/T`).

---

## Анимации людей Mixamo (2026-10-12) — `export/anim/anims_mixamo.glb`

Папка Диска «15 Анимации»: 62 FBX + 3 набора (Action Adventure, Scary Zombie, Creature NPC). `Dewier…zip` и `luna pack.zip`
не скачивал и не трогал. Итог — **106 действий в одном файле** (скелет + действия, без сетки, 30 кадров/с), 12,8 МБ.
Лист: `renders/_review/anims_2026-10-12.jpg` — 12 поз на `body_m_rig`.

**Как сделано:**
1. `tools/anims_mixamo.py` — импорт FBX, сетка удаляется, действие получает имя из `docs/ANIMATIONS.md`; сантиметры FBX →
   метры; все действия на одном скелете Mixamo → `tripo/anims_mixamo_src.glb` (в git не идёт).
2. `tools/anims_retarget.py` — **перенос на скелет тел Tripo** (`body_m_rig`). Имена костей те же, но в позе покоя кости
   Mixamo и Tripo смотрят в разные стороны: без переноса тело получалось с задранной рукой и раскоряченными ногами.
   Каждая кость получает тот же поворот в мире, что у Mixamo (с поправкой на позу покоя), корень двигается в масштабе роста
   (×0,92). Итог — `export/anim/anims_mixamo.glb` на скелете Tripo: проверено на `body_m_rig` (лист); у остальных тел Tripo
   (`body_m_rig_b`, `body_f_rig`, `char_f_hoodie`, `body_m_rig_c`) та же поза покоя и кости — анимации Tripo между ними
   переходили без поправок, так что и эти должны подойти без настройки перенаправления в игре.
3. В файле крошечный невидимый треугольник на Hips — без привязанной сетки glTF пишет кости обычными узлами, не скелетом.

**Кости:** во всех FBX одинаковые — 65 костей `mixamorig:…`, совпадают с телами Tripo. У `body_m_rig(_b)` есть ещё служебная
`neutral_bone` (её анимации не двигают); у `body_m_rig_c` нет 11 концевых костей (кончики пальцев `…4`, `HeadTop_End`) —
не мешает.

**«На месте» — пришлось чинить 25** (корень уезжал вперёд, обнулено движение Hips по горизонтали, высота оставлена):
`aa_run` (3.32 м), `aa_walk` (1.85 м), `cover_sneak_l` (1.34 м), `cover_sneak_r` (1.34 м), `crawl` (0.91 м), `injured_run` (1.56 м), `injured_walk` (2.09 м), `injured_walk_b` (0.92 м), `injured_walk_c` (1.79 м), `jog` (5.07 м), `mutant_run` (2.06 м), `mutant_walk` (1.88 м), `rifle_walk` (4.32 м), `sneak` (1.34 м), `sneak_l` (1.34 м), `sneak_r` (1.21 м), `strafe` (2.09 м), `swim` (2.19 м), `walk_b` (2.8 м), `walk_c` (2.8 м), `walk_turn` (1.14 м), `zombie_crawl` (2.22 м), `zombie_crawl_run` (1.45 м), `zombie_run` (2.48 м), `zombie_walk` (1.38 м).
На месте с самого начала: `walk`, `run` (и остальные не из списка ходьбы/бега).

**Что такое `entry`:** пригибается, шагает вперёд, будто пролезает в низкий проём (лаз, люк), и выпрямляется.

**Не по таблице:**
- Action Adventure Pack: idle-файлов **5**, а не 6 → `aa_idle_1…5` (`aa_idle_6` нет).
- Вторые копии: `stand to cover (2)` → `to_cover_b`, `cover to stand (2)` → `from_cover_b`; в Creature NPC Pack лишние
  `left turn 45` → `mutant_turn_l_b`, `mutant right turn 45 (2)` → `mutant_turn_r_b`.
- Не взяты: `Idle.fbx` (со скином, взят меньший `Idle (1)`), `zombie neck bite` из набора (есть отдельный файл),
  `X Bot.fbx` ×2 (манекен).
- Проверить в игре: у `dig` голова наклонена очень сильно (так в Mixamo или от переноса — на листе видно).

**Ещё нет (автор докачает):** `eat`, `mine`, `surrender`, `throw`, `rifle_idle`, `rifle_shoot`, `sit`.

| Имя | Файл | Кадров | Сек |
|---|---|---|---|
| `aa_idle_1` | Action Adventure Pack/idle | 117 | 3.87 |
| `aa_idle_2` | Action Adventure Pack/idle (2) | 298 | 9.9 |
| `aa_idle_3` | Action Adventure Pack/idle (3) | 98 | 3.23 |
| `aa_idle_4` | Action Adventure Pack/idle (4) | 78 | 2.57 |
| `aa_idle_5` | Action Adventure Pack/idle (5) | 69 | 2.27 |
| `aa_run` | Action Adventure Pack/running | 22 | 0.7 |
| `aa_walk` | Action Adventure Pack/walking | 32 | 1.03 |
| `bow_shoot` | Shooting Arrow | 151 | 5.0 |
| `carry_turn` | Carrying Turn | 117 | 3.87 |
| `climb` | Climbing Ladder | 24 | 0.77 |
| `climb_down` | Climbing Down | 104 | 3.43 |
| `climb_wall` | Climbing | 116 | 3.83 |
| `cover_sneak_l` | Action Adventure Pack/left cover sneak | 35 | 1.13 |
| `cover_sneak_r` | Action Adventure Pack/right cover sneak | 35 | 1.13 |
| `crawl` | Crawling | 55 | 1.8 |
| `crouch_to_stand` | Crouch To Stand | 101 | 3.33 |
| `death` | Dying | 133 | 4.4 |
| `death_b` | Standing Death Left 01 | 69 | 2.27 |
| `dig` | Digging | 146 | 4.83 |
| `drink` | Drinking | 267 | 8.87 |
| `entry` | Entry | 220 | 7.3 |
| `fall` | Action Adventure Pack/falling idle | 22 | 0.7 |
| `fall_roll` | Action Adventure Pack/falling to roll | 45 | 1.47 |
| `float` | Floating | 109 | 3.6 |
| `from_cover` | Action Adventure Pack/cover to stand | 46 | 1.5 |
| `from_cover_b` | Action Adventure Pack/cover to stand (2) | 35 | 1.13 |
| `gunplay` | Gunplay | 96 | 3.17 |
| `hang_climb` | Freehang Climb | 117 | 3.87 |
| `harvest` | Pick Fruit | 187 | 6.2 |
| `hit` | Rib Hit | 31 | 1.0 |
| `hit_big` | Standing React Large From Front | 31 | 1.0 |
| `hit_head` | Head Hit | 44 | 1.43 |
| `idle` | Idle (1) | 60 | 1.97 |
| `idle_look` | Unarmed Idle Looking Ver. 2 | 236 | 7.83 |
| `injured_run` | Injured Run | 20 | 0.63 |
| `injured_walk` | Injured Walk | 50 | 1.63 |
| `injured_walk_b` | Injured Walk (1) | 36 | 1.17 |
| `injured_walk_c` | Injured Walking | 31 | 1.0 |
| `jog` | Jogging | 78 | 2.57 |
| `jump` | Jump | 66 | 2.17 |
| `jump_down` | Jumping Down | 116 | 3.83 |
| `jump_up` | Action Adventure Pack/jumping up | 8 | 0.23 |
| `kneel` | Kneeling Down | 84 | 2.77 |
| `land_hard` | Action Adventure Pack/hard landing | 61 | 2.0 |
| `melee` | Standing Melee Attack Downward | 69 | 2.27 |
| `mutant_death` | Creature NPC Pack/mutant dying | 139 | 4.6 |
| `mutant_idle` | Creature NPC Pack/mutant idle | 160 | 5.3 |
| `mutant_idle_b` | Creature NPC Pack/mutant breathing idle | 122 | 4.03 |
| `mutant_jump` | Creature NPC Pack/mutant jumping | 96 | 3.17 |
| `mutant_roar` | Creature NPC Pack/mutant flexing muscles | 141 | 4.67 |
| `mutant_run` | Creature NPC Pack/mutant run | 27 | 0.87 |
| `mutant_swipe` | Creature NPC Pack/mutant swiping | 81 | 2.67 |
| `mutant_turn_l` | Creature NPC Pack/mutant left turn 45 | 41 | 1.33 |
| `mutant_turn_l_b` | Creature NPC Pack/left turn 45 | 41 | 1.33 |
| `mutant_turn_r` | Creature NPC Pack/mutant right turn 45 | 60 | 1.97 |
| `mutant_turn_r_b` | Creature NPC Pack/mutant right turn 45 (2) | 41 | 1.33 |
| `mutant_walk` | Creature NPC Pack/mutant walking | 44 | 1.43 |
| `open_box` | Opening | 330 | 10.97 |
| `open_door` | Open Door Outwards | 124 | 4.1 |
| `pick_up` | Picking Up Object | 104 | 3.43 |
| `pick_up_floor` | Unarmed Grab Torch From Floor | 116 | 3.83 |
| `pistol_shoot` | Shooting Gun | 160 | 5.3 |
| `punch` | Illegal Elbow Punch | 69 | 2.27 |
| `punch_combo` | Punching Bag | 98 | 3.23 |
| `push` | Push | 52 | 1.7 |
| `rifle_walk` | Walk With Rifle | 102 | 3.37 |
| `run` | Fast Run | 17 | 0.53 |
| `run_stop` | Action Adventure Pack/run to stop | 27 | 0.87 |
| `search` | Rummaging | 146 | 4.83 |
| `search_low` | Looking Through Files Low | 433 | 14.4 |
| `sit_injured` | Sitting Rubbing Arm | 240 | 7.97 |
| `sit_talk` | Sitting Talking | 1323 | 44.07 |
| `sleep` | Sleeping Idle | 207 | 6.87 |
| `sneak` | Crouched Sneaking Left | 39 | 1.27 |
| `sneak_l` | Action Adventure Pack/crouched sneaking left | 39 | 1.27 |
| `sneak_r` | Action Adventure Pack/crouched sneaking right | 33 | 1.07 |
| `stab` | Double Dagger Stab | 93 | 3.07 |
| `stand_up` | Standing Up | 183 | 6.07 |
| `strafe` | Strafe | 36 | 1.17 |
| `swim` | Swimming | 137 | 4.53 |
| `talk` | Talking | 156 | 5.17 |
| `talk_b` | Talking (1) | 114 | 3.77 |
| `taunt` | Taunt | 98 | 3.23 |
| `to_cover` | Action Adventure Pack/stand to cover | 35 | 1.13 |
| `to_cover_b` | Action Adventure Pack/stand to cover (2) | 39 | 1.27 |
| `turn_l` | Action Adventure Pack/left turn | 32 | 1.03 |
| `turn_r` | Action Adventure Pack/right turn | 32 | 1.03 |
| `walk` | Walking | 32 | 1.03 |
| `walk_b` | Walking (1) | 87 | 2.87 |
| `walk_c` | Walking (2) | 87 | 2.87 |
| `walk_turn` | Walk Forward Arc Right | 45 | 1.47 |
| `work_counter` | Bartending | 408 | 13.57 |
| `work_counter_b` | Bartending (1) | 408 | 13.57 |
| `work_table` | Working On Device | 194 | 6.43 |
| `zombie_attack` | Scary Zombie Pack/zombie attack | 76 | 2.5 |
| `zombie_bite` | Scary Zombie Pack/zombie biting | 199 | 6.6 |
| `zombie_bite_b` | Scary Zombie Pack/zombie biting (2) | 70 | 2.3 |
| `zombie_crawl` | Scary Zombie Pack/zombie crawl | 155 | 5.13 |
| `zombie_crawl_run` | Scary Zombie Pack/running crawl | 20 | 0.63 |
| `zombie_death` | Scary Zombie Pack/zombie death | 85 | 2.8 |
| `zombie_dying` | Scary Zombie Pack/zombie dying | 100 | 3.3 |
| `zombie_idle` | Scary Zombie Pack/zombie idle | 129 | 4.27 |
| `zombie_neck_bite` | Zombie Neck Bite | 126 | 4.17 |
| `zombie_run` | Scary Zombie Pack/zombie run | 25 | 0.8 |
| `zombie_scream` | Scary Zombie Pack/zombie scream | 85 | 2.8 |
| `zombie_walk` | Scary Zombie Pack/zombie walk | 122 | 4.03 |

---

## Персонажи со скелетом (2026-10-13) — `renders/_review/rigged_chars_2026-10-13.jpg`

Автор загрузил в «13 Персонажи и существа» 53 файла с ригом Tripo (Гуманоид, Mixamo). Опознаны по сетке (то же число
треугольников и точек, что у уже обработанных), имена — прежние. **52 со скелетом** (65–66 костей `mixamorig:…`),
`old+man+3d+model (2)` (= `char_iw_m_old`) — **без скелета**, остался статичным.

- `tools/char_process.py --rot 0`: у моделей с ригом Tripo перед уже к камере (поворот 270°, как у статичных, ставил их
  боком — переделано). Рост — как у статичных версий. `_idle.glb` — сетка + скелет, 0,66–0,82 МБ, анимаций внутри нет.
- **`tools/rig_normalize.py` — поза покоя выровнена по `body_m_rig`.** Tripo строит каждому свой скелет: кости те же, но в
  покое руки и пальцы под другим углом, и общая анимация задирала руку (было у 7: `char_f_police_b`, `char_free_m_office`,
  `char_gr_m`, `char_prisoner_m_old`, `char_s9_m_subject`, `char_iw_f`, `char_free_f_rain`). Теперь у всех 52 поза покоя
  как у эталона — `export/anim/anims_mixamo.glb` ложится на всех одинаково (лист: все идут, руки внизу).
- Статичные версии этих 52 заменены (тот же файл `export/<имя>_idle.glb`).

**Ещё без скелета (20):** `char_f_mechanic`, `char_f_military`, `char_f_military_b`, `char_fm_m`, `char_fm_m_young`, `char_free_f_denim`, `char_gr_m_big`, `char_iw_m_old`, `char_m_adventurer`, `char_m_hoodie`, `char_m_military`, `char_m_military_b`, `char_m_tactical`, `char_rd_m_thin`, `char_rd_raider`, `char_s9_f`, `char_s9_m_guard`, `char_ws_m_old`, `zombie_office`, `zombie_runner`.

### Дозагрузка с ригом (2026-10-13, вторая)

Ещё **9 персонажей со скелетом**: `char_f_mechanic`, `char_fm_m`, `char_fm_m_young`, `char_free_f_denim`, `char_gr_m_big`,
`char_iw_m_old`, `char_s9_f`, `char_s9_m_guard`, `char_ws_m_old` — опознаны по сетке, `char_process --rot 0`, поза покоя
выровнена (`rig_normalize`), ходьба проверена.

⚠ **Риг Tripo сломан у скелетов из 54 костей** — `zombie_runner` и `body_m_rig_c`: Tripo не привязал сетку к костям, вся
сетка висит на одной кости Hips (руки и ноги не двигаются). Пробовал перенести привязку с `body_m_rig` — у тела искажается
плечо, у зомби руки гнутся неправильно и тянутся лишние кусочки сетки; не годится. `zombie_runner` оставлен статичным,
`body_m_rig_c` — как был (анимации на нём не работают). Их нужно **заригать заново** в Tripo (или на mixamo.com).
`tools/rig_normalize.py`: добавлено выравнивание поворота кости вокруг своей оси (roll) без движения сетки.

**Ещё без скелета (11):** `char_f_military`, `char_f_military_b`, `char_m_adventurer`, `char_m_hoodie`, `char_m_military`,
`char_m_military_b`, `char_m_tactical`, `char_rd_m_thin`, `char_rd_raider`, `zombie_office`, `zombie_runner` (риг сломан).

**Диск:** файлы с ригом в «13 Персонажи и существа» названы как в проекте (`<имя>.glb`), прежние версии без рига — в
«Дубли» с пометкой «(без рига)»; `tripo/drive.json` указывает на версии с ригом.

**2026-10-13, решение автора:** 11 персонажей без рабочего рига удалены (не важны): `char_f_military`, `char_f_military_b`,
`char_m_military`, `char_m_military_b`, `char_m_adventurer`, `char_m_tactical`, `char_rd_m_thin`, `char_rd_raider`,
`zombie_office`, `zombie_runner`, `body_m_rig_c`. На Диске — в корзине (30 дней можно вернуть). `char_m_hoodie` пока
оставлен — статичный, без скелета.

### Анимации — проверка и исправления (2026-10-13)

- **Рывки:** знак поворота кости (q / −q) менялся между кадрами — между кадрами движок крутил кость «длинным путём».
  Исправлено во всех `export/anim/*.glb` (`tools/glb_quat_fix.py`): 3 623 места в `anims_mixamo`, 9 216 в анимациях тел.
- **«На месте» было слишком грубо:** у 25 ходьб/бегов обнулялось всё движение таза по горизонтали — пропадало
  покачивание бёдер, походка деревянная. Теперь убирается только равномерный уезд вперёд, покачивание осталось.
- **Сверка с оригиналом:** `renders/_review/anims_compare_2026-10-13.jpg` — `walk` и `run` на манекене Mixamo (X Bot) и на
  теле Tripo, кадр в кадр: позы совпадают, перенос верный.
- Для игры: родная скорость ходьбы/бега — `anims_mixamo_info.json` → `speed_mps` (`walk` 1,77 м/с, `run` 5,43), иначе
  ноги скользят; анимации уже на скелете тел Tripo — в Godot **не включать** ещё одно перенаправление (retarget/BoneMap)
  поверх, иначе позы исказятся.

## Животные: скелет и анимации (2026-10-13) — `renders/_review/animals_2026-10-13.jpg`

Tripo/Mixamo не делают риг для зверей, поэтому скелет и анимации делает `tools/animal_rig.py` (сам, без ручной работы):
- по сетке находятся лапы (следы на полу), живот и спина, голова (впереди передних лап), хвост, у птиц — крылья;
- ставятся кости: звери — 18 (таз, спина, шея, голова, хвост ×2, 4 лапы × 3), птицы — 9 (тело, голова, хвост, крылья ×2, лапы);
- каждой вершине — веса ближайших костей (лапа не тянет соседнюю лапу), сглажено по сетке;
- анимации по формулам, внутри того же `export/<id>_idle.glb`.

| Группа | Кто | Анимации |
|---|---|---|
| Звери (20) | dog_feral_odinochnaya, dog_husky, dog_raider, dog_rottweiler, dog_shepherd, dog_terrier, dog_thin, dog_zombie, wolf, bear_black/brown/mutant, deer_red/roe/white, moose_bull/cow/mutant, rat_grey, rat_pest_krysa | idle, walk (шаг), run (галоп), eat, attack (бросок), hit, death (на бок) |
| Зайцы (4) | rabbit_grey, rabbit_hare, rabbit_white, rabbit_wild_krolik | idle, walk и run (прыжками), eat, hit, death |
| Птицы (6) | crow, pigeon, seagull, vulture, owl, duck | idle и walk (крылья сложены), fly (машет), eat (клюёт), hit, death |

Файлы 0,3–1,5 МБ. Скорость ходьбы/бега на месте и длительности — `export/anim/animals_info.json`.
Сырые модели без костей — `tripo/static/` (не в git), из них скрипт пересобирает заново.
Не сделано: `mutant_crawler_polzun` (не зверь — существо с руками, нужен свой риг).

## Анимации людей на одетых персонажах (2026-10-14) — `renders/_review/anims_clothed_fix_2026-10-14.jpg`

Проверка «как в игре» (`tools/anim_check.py`: кадр собирается из glTF так же, как в Godot) показала три беды:
1. В анимациях у каждой кости было записано и **место** (длины костей голого тела) — у одетых и полных персонажей
   плечи сужались, руки уходили в тело, рост менялся. Теперь только повороты + таз (`tools/glb_strip_tracks.py`,
   встроено в `anims_retarget.py` и `char_process.py`).
2. **Локоть пережат:** у скелетов Tripo в покое локти/колени/спина чуть согнуты (локоть ~20°), перенос прибавлял это к
   каждой анимации. Теперь каждая кость в покое смотрит на следующий сустав как у Mixamo — сгибы как в оригинале
   (ходьба: локоть 39° вместо 57°).
3. Анимации Mixamo — для худого голого тела: у полных/в куртках руки проходят сквозь живот. `tools/char_fit.py` для
   каждого персонажа ставит его в позы анимаций и подбирает угол отведения плеч (`arm_spread_deg`, 0–16°) + высоту
   таза (`motion_scale`) → `export/anim/char_fit.json`; применяет игра (FOR_GAME.md).

## Руки без сужения в плече и локте (2026-10-14) — `renders/_review/arms_native_mesh_2026-10-14.jpg`

Автор: «руки слишком сужены вверху и в локте». Причина — `rig_normalize.py`: он переставлял руки персонажа в позу
голого тела и «запекал» это в сетку, а сетка в сгибах при таком переносе сплющивается. Для игры это не нужно (Godot берёт
из анимации повороты, поза покоя не важна) — нужна была только одинаковая ось кости. Новый `tools/rig_roll.py`
поворачивает каждую кость вокруг её же оси (у Tripo расхождение до 180°), сетка остаётся родной. Пересобраны все 61
(52 — из версии до выравнивания, 9 — заново из файлов с ригом с Диска). Анимации и прочее не трогал; `char_fit.json`
пересчитан под новую сетку.

## Партия 2026-10-14 («новое», 28 файлов) — `renders/_review/tripo_2026-10-14_new.jpg`

Запросы — `docs/TRIPO_STREET_2026-10-14.md`. Файлы опознаны по виду, названы по списку, обработаны `tripo_process.py`
(настройки — `tripo/extra.json`, повороты — `rotate.json`), на Диске переименованы и разложены:

| Папка Диска | Модели (export/<имя>_idle.glb) |
|---|---|
| 19 Природа (деревья, паром) | `tree_oak`, `tree_birch`, `tree_maple`, `tree_dead_bare`, `tree_dead_bare_b`, `tree_dead_burnt`, `tree_dead_stump`, `ferry_raft`, `ferry_raft_b` |
| 20 Улица — островки | `isle_dumpster`, `isle_trash_bins`, `isle_barrels_fire`, `isle_scrap`, `isle_scrap_b`, `isle_pallets`, `isle_pallets_b`, `isle_bench_bin` |
| 21 Поезд | `train_loco_diesel`, `train_coach`, `train_coach_b…e` (4 других вагона), `train_freight`, `train_freight_b` |
| 12 Предметы… | `bow_modern`, `bow_wood_simple` |
| 10 Декор-объекты | `decor_camp_chair` (раскладной стул — не из списка) |

- Деревья — 8 000 треуг., вагоны и тепловоз — 15 000 (поставлены боком, длинной стороной вдоль X), островки и паром — 8 000, луки и стул — 3 000. Файлы 0,17–0,83 МБ.
- Вагонов пришло 7 вместо 3 (пробы): лишние названы `train_coach_b…e`, `train_freight_b`. Паром — 2 варианта.
- ⚠ `tree_dead_burnt` — сухое дерево светлое, не чёрное обгоревшее; `tree_dead_stump` — высокий обломанный ствол (в списке не было).
- Не пришли: островки `isle_fence_tires`, `isle_hydrant`, `isle_mailbox`, `isle_bikes`, `isle_roadworks`, `isle_planter`.

## Животные: новые анимации (2026-10-14) — `renders/_review/animals_2026-10-14.jpg`

`tools/animal_rig.py`: звери — `flee`, `sit`, `lie_down`, `sleep`; зайцы — `attack`, `beg`; собаки и волк — `howl`,
`growl`, `beg`; медведи — `growl`; птицы — `takeoff`, `glide`, `sit`, `sleep`, `attack`, `flee`. Итого у собак и волка
14 анимаций, у медведей 12, у оленей/лосей/крыс 11, у зайцев и птиц 12. `rabbit_wild_krolik` (модель уже сидит
столбиком) — мягкие позы: пригибается, опускает голову, поднимает лапки. Лист: покой · сидит · лёг · спит · убегает ·
атакует · рычит · воет · просит (у птиц: взлёт · парит · сидит · спит · атакует · убегает).

## Мелочи кодом: улица и следы (2026-10-14) — `renders/_review/street_props_2026-10-14.jpg`

`tools/make_props_street.py` (заготовки и «нарисованная» текстура — из `make_props.py`): бордюры (прямой, угол),
разметка (полоса, переход), столб ЛЭП и провода пролётом, рельсы — тупик и переезд (поворот не делал: мир виден сбоку,
рельсы идут вдоль), цепь висящая и кучей, верёвка с петлёй, кабели по полу и с потолка, кости, сугроб, снег пятном,
следы в грязи и на снегу. 18 моделей, 12–2 300 треугольников, 8–220 КБ.

### Исправлено (2026-10-14, по замечанию автора «сидит, просит еду — неправильно»)

Разбор по кадрам (сбоку и в 3/4): при посадке задняя лапа висела в воздухе, хвост уходил в пол, голова — мордой в
небо, поданная лапа торчала прямой палкой. Позы `sit`, `beg`, `lie_down`, `sleep` (и `howl`, он на основе `sit`)
переделаны на **обратную кинематику**: задаются точки, где стоят лапы (на полу под плечом / под тазом, скакательный
сустав и стопа — на полу), суставы сгибаются сами, наклон тела и опускание таза подбираются так, чтобы передние лапы
стояли, а таз был у пола; голова держится ровно, хвост лежит на полу. Поданная лапа — согнута в запястье, кисть
свисает. Заяц «просит» — встаёт столбиком, лапки поджаты. Копытные лежат с подогнутыми передними ногами.

### Исправлено (2026-10-15): ноги проваливались под пол

Замер по каждому кадру: в позах «сидит/лежит» сложенные ноги уходили под пол (собака 10 см, медведь 25, олень и лось
27–34), при ходьбе и беге — 2–8 см. Теперь позы подбираются **по самой сетке**: перебор наклона тела, высоты таза и
сгиба колена, каждая проба примеряется — зад и бедро на полу (не ниже), передние и задние лапы на полу. Задняя нога
сидящего зверя — бедро вперёд-вверх, голень вниз до пола, стопа лежит вперёд. Плюс проверка всех анимаций по кадрам:
если что-то ниже пола — корень поднимается ровно на столько (`ground_fix`). Итог по замеру: 0 см под полом во всех
анимациях у всех 30. Лист — `renders/_review/animals_2026-10-15.jpg`.

### 2026-10-15: возврат к прошлой версии поз

Подбор поз по сетке (ноги не уходят под пол) дал неестественную посадку — автор: «бред, верни как было». Возвращена
версия от 14.10 (лапы ставятся в точки на полу); подача лапы у собак и волка удалена. Все 30 пересобраны.

## Открывающиеся модели (2026-10-15) — `renders/_review/open_parts_*_2026-10-15.jpg`

- Инструмент `tools/open_parts.py`, настройки `tripo/open_parts.json` (для каждой модели: что отрезать, где петля,
  как открывается, что вырезать внутри, чем «нарисовано» внутри — доски / металл / пластик).
- Результат: `export/parts/<имя>.glb` (корпус `body` + части), `export/parts/open_parts.json` — оси и углы для игры.
- Листы «закрыто / открыто»: `open_parts` (шкаф, ящик, вагон), `_A` (шкафчики, холодильник, плиты, сейф, щиты),
  `_B` / `_B2` (ящики, баки, аптечки), `_C` (люки, двери), `_D` (вагоны), `_E` / `_E2` (машины), `_F` (будки,
  контейнер, решётка, гаражи, колодец, насос).
- Ограничения: внутри — простая пустота с текстурой досок/металла (Tripo делает только оболочку); у машин —
  простые коробки-сиденья; у тепловоза и `train_coach_c` дверей нет (на модели не видно, где резать — пропущены).
