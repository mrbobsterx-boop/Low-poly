# Отчёт обработки моделей из Tripo

Делает `tools/tripo_process.py` (правила — `docs/TRIPO.md`, раздел 2). Данные — `docs/tripo_report.json`.

| Модель (export/) | Файл из tripo/ | Треугольники до → после (лимит) | Размер Ш × Г × В, см | ОС Ш × В, см | Масштаб | Поворот | Крепление | Текстуры | Файл, МБ | Предупреждения |
|---|---|---|---|---|---|---|---|---|---|---|
| `recycler_bench_ruchnoy_idle` | `recycler_bench_ruchnoy.glb` | 90 165 → 7 839 (8 000) | 220 × 153 × 95 | 130 × 95 | ×2.24 | 270° | floor | 3 шт. 2048→1024 | 0.53 | ⚠ ширина 220 см  в ОС 130 см (> 15 %) — записано в DEVIATIONS.md |
| `room_bunker_wall_1_idle` | `room_bunker_wall_1.glb` | 14 509 → 3 920 (4 000) | 320 × 30 × 300 | — × 300 | ×3.34 | 270° | стена комнаты | 3 шт. 2048→1024 | 0.41 | — |
| `room_bunker_wall_3_idle` | `room_bunker_wall_3.glb` | 46 233 → 3 918 (4 000) | 328 × 30 × 300 | — × 300 | ×3.43 | 270° | стена комнаты | 3 шт. 2048→1024 | 0.57 | — |
| `room_bunker_wall_4_idle` | `room_bunker_wall_4.glb` | 46 094 → 3 918 (4 000) | 304 × 30 × 300 | — × 300 | ×3.17 | 270° | стена комнаты | 3 шт. 2048→1024 | 0.43 | — |
| `room_bunker_wall_5_idle` | `room_bunker_wall_5.glb` | 47 250 → 3 920 (4 000) | 265 × 30 × 300 | — × 300 | ×3.1 | 90° | стена комнаты | 3 шт. 2048→1024 | 0.48 | — |
| `sewing_table_pedalnaya_idle` | `sewing_table_pedalnaya.glb` | 87 414 → 7 840 (8 000) | 89 × 55 × 85 | 110 × 85 | ×0.906 | 270° | floor | 3 шт. 2048→1024 | 0.66 | ⚠ ширина 89 см  в ОС 110 см (> 15 %) — записано в DEVIATIONS.md |
| `sewing_table_ruchnaya_mashina_idle` | `sewing_table_ruchnaya_mashina.glb` | 88 842 → 7 838 (8 000) | 114 × 68 × 85 | 110 × 85 | ×1.17 | 270° | floor | 3 шт. 2048→1024 | 0.59 | — |
| `workbench_basic_derevyannyy_bazovyy_idle` | `workbench_basic_derevyannyy_bazovyy.glb` | 82 519 → 7 840 (8 000) | 181 × 86 × 95 | 160 × 95 | ×1.85 | 270° | floor | 3 шт. 2048→1024 | 0.68 | — |
| `workbench_basic_metallicheskiy_idle` | `workbench_basic_metallicheskiy.glb` | 84 229 → 7 840 (8 000) | 155 × 100 × 95 | 160 × 95 | ×1.58 | 270° | floor | 3 шт. 2048→1024 | 0.65 | — |
| `workbench_basic_skladnoy_pohodnyy_idle` | `workbench_basic_skladnoy_pohodnyy.glb` | 93 380 → 7 840 (8 000) | 152 × 93 × 95 | 160 × 95 | ×1.55 | 270° | floor | 3 шт. 2048→1024 | 0.62 | — |
| `workbench_basic_verstak_s_tiskami_idle` | `workbench_basic_verstak_s_tiskami.glb` | 81 380 → 7 840 (8 000) | 169 × 115 × 95 | 160 × 95 | ×1.72 | 270° | floor | 3 шт. 2048→1024 | 0.60 | — |
| `workbench_electronics_mobilnaya_stoyka_idle` | `workbench_electronics_mobilnaya_stoyka.glb` | 82 662 → 7 840 (8 000) | 189 × 66 × 95 | 140 × 95 | ×1.93 | 270° | floor | 3 шт. 2048→1024 | 0.66 | ⚠ ширина 189 см  в ОС 140 см (> 15 %) — записано в DEVIATIONS.md |
| `workbench_electronics_nastolnyy_idle` | `workbench_electronics_nastolnyy.glb` | 84 157 → 7 840 (8 000) | 122 × 64 × 95 | 140 × 95 | ×1.24 | 270° | floor | 3 шт. 2048→1024 | 0.67 | — |
