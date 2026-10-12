# Партия 2026-10-12 — имена файлов (для второго чата)

Запросы — в чате с автором и в `TRIPO_CHARACTERS.md` (№ 93–164). Здесь — **как назвать и как резать**.
Наборы «3 на одной картинке» (и 6 птиц) — **резать слева направо** (у птиц: верхний ряд, потом нижний) на отдельные
модели, как двери; каждой — своё имя из списка. Если автор уже разрезал картинку сам и прислал по одной — просто назвать.

## 1. Наборы вещей (без рига) → резать на 3

| Файл набора | Слева → направо |
|---|---|
| `set_fm_1` | `hat_fm_sou`, `hat_fm_hood`, `mask_fm_tally` |
| `set_fm_2` | `hat_fm_wide`, `back_fm_rope`, `belt_fm_lantern` |
| `set_gr_1` | `hat_gr_net`, `hat_gr_boonie`, `hat_gr_beret` |
| `set_gr_2` | `goggles_gr`, `back_gr_radio`, `mask_gr_gas` |
| `set_s9_1` | `mask_s9_visor`, `hat_s9_hood`, `hat_s9_helmet` |
| `set_s9_2` | `goggles_s9`, `back_s9_air`, `back_s9_case` |
| № 197 | `back_sack_ore`, `back_basket_coal`, `back_firewood` |
| № 198 | `tool_pick_old`, `tool_shovel_old`, `item_bucket_wood` |
| № 199 | `wrist_rope`, `wrist_shackles`, `back_yoke_buckets` |
| № 200 | `item_tray_food`, `item_mug_tin`, `back_bedroll_prison` |
| № 201 | `tool_sledgehammer`, `tool_broom_push`, `item_mop_bucket` |
| № 202 | `item_handcuffs`, `weapon_shiv`, `item_contraband` |
| ковры | `rug_persian`, `rug_round_braided`, `rug_bear_skin` |

Вещи на человека (`hat_`, `mask_`, `goggles_`, `back_`, `belt_`, `wrist_`) — точка опоры **в месте крепления**
(шапка — низ по центру, рюкзак — середина спинки, маска — центр задней стороны), размер — **настоящий**
(шапка ≈ 0,2–0,3 м, рюкзак ≈ 0,5 м). Остальное — как обычные предметы.

## 2. Уголки и стыки (без рига) → резать на 3

| Файл набора | Слева → направо |
|---|---|
| `joint_pipes_set_1` | `joint_pipes_L_up`, `joint_pipes_L_down`, `joint_pipes_T_up` |
| `joint_pipes_set_2` | `joint_pipes_T_down`, `joint_pipes_X`, `pipes_end_caps` |
| `joint_pipes_set` (№ 188, старый вариант) | `joint_pipes_L`, `joint_pipes_T`, `joint_pipes_X` |
| `joint_duct_set` | `joint_duct_L`, `joint_duct_T`, `joint_duct_X` |
| `joint_duct_set_b` | `joint_duct_up`, `duct_end_cap`, `duct_end_grille` |
| `joint_misc_set` (№ 189) | `joint_cablech_L`, `joint_duct_L_alt`, `joint_beam_L` |
| `joint_misc_set_b` (№ 190) | `joint_molding_L`, `mine_rails_curve`, `fence_post_corner` |

**Сечение уголка = сечению прямого куска** (`decor_pipes_colored_h/v`, `decor_metal_duct`, `decor_cable_channel`,
`decor_steel_beam`, `decor_wood_molding` в игре): подогнать масштаб так, чтобы ширина и толщина ветки совпали с прямым
куском **точно**; центр стыка — в начале координат, ветки — по осям X (вправо/влево) и Y (вверх/вниз), задняя сторона —
к стене (−Z). Трубы: в горизонтали сверху вниз жёлтая, синяя, красная; в вертикали слева направо жёлтая, синяя,
красная — если на модели не так, записать в отчёт.

## 3. Люди с ригом (Tripo «Гуманоид», Mixamo) → `tools/char_process.py`

- Фракции: № 93–164 (`TRIPO_CHARACTERS.md`, `char_<фракция>_…`).
- Без фракции: `char_free_f_rain`, `char_free_m_hermit`, `char_free_f_denim`, `char_free_m_office`,
  `char_free_m_hunter`, `char_free_f_nurse`, `char_free_m_teacher`.
- Шахтёры: `char_miner_m`, `char_miner_m_big`, `char_miner_f`, `char_miner_m_old`, `char_miner_f_young`.
- Зомби: `zombie_office`, `zombie_hospital`, `zombie_fat`, `zombie_firefighter`, `zombie_runner`.
- Рабы: `char_slave_m`, `char_slave_f`, `char_slave_m_old`. Заключённые: `char_prisoner_m`, `char_prisoner_f`,
  `char_prisoner_m_old`.

Скелет оставить как есть (длинная кость «макушка» над головой — не ошибка, не трогать). Рост ≈ 1,8 м (женщины ≈ 1,7,
здоровяки — по модели), ступни на y = 0, лицом к −Y (в Godot — к камере). Имя файла без анимаций — `<имя>_idle.glb`.
Анимации — потом отдельной папкой (Mixamo, «Without Skin»), их не ждать.

## 4. Животные — пока **без рига**, как обычные модели

`dog_shepherd`, `dog_feral`, `dog_terrier`, `dog_zombie`, `dog_husky`, `dog_raider`, `bear_brown`, `bear_black`,
`bear_mutant`, `rat_grey`, `rat_big`, `rat_mutant`, `rabbit_hare`, `rabbit_white`, `rabbit_grey`, `crow`, `pigeon`,
`seagull`, `vulture`, `owl`, `duck`, `deer_red`, `deer_roe`, `deer_white`, `moose_bull`, `moose_cow`, `moose_mutant`.

Если пришла модель с ригом Tripo (собака) — **риг выкинуть** (он кривой), оставить сетку. Размер — настоящий (овчарка
≈ 0,65 м в холке, медведь ≈ 1,1–1,5, лось ≈ 2, крыса ≈ 0,25 в длину, кролик ≈ 0,4, ворона ≈ 0,45), стоит на y = 0,
мордой к −Y. Скелет четвероногого — **отдельным заданием потом**.
