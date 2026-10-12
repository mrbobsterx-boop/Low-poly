# Анимации людей (Mixamo) — как обработать

Папка Диска **«15 Анимации»** `1STfM0xIPkg-Knkd2dcMqteNyI7vdmL9d`: FBX из Mixamo по одному + 3 набора zip
(Action Adventure Pack, Scary Zombie Pack, Creature NPC Pack). **Не анимации, не трогать:** `Dewier_20K_Modified_T-Packs.zip`,
`luna pack.zip` (чужие текстуры и модели другой игры — в проект не брать).

`drive_fetch.py` качает только glb/png — для этой папки скачать FBX и zip отдельно (тем же адресом
`https://drive.usercontent.google.com/download?id=<id>&export=download&confirm=t`).

## Что сделать

1. Для каждой анимации из таблицы — Blender: импорт FBX, **удалить сетку** (если скачано «With Skin»), оставить скелет
   Mixamo и действие (Action), назвать действие **именем из таблицы**.
2. Проверить «на месте»: у ходьбы / бега / ползания корень (Hips) не должен уезжать вперёд. Уезжает — обнулить движение
   Hips по горизонтали (X/Z в Blender — X/Y), высоту оставить. Записать в отчёт, какие пришлось чинить.
3. Все действия — **в один файл** `export/anim/anims_mixamo.glb` (скелет + все действия, без сетки), 30 кадров/с.
   Зомби и мутанты — туда же (имена `zombie_…`, `mutant_…`).
4. Сверить имена костей с телами Tripo со скелетом (`body_m_rig_idle.glb`): должны совпадать (`mixamorig:Hips`…).
   Не совпадают — в отчёт, какие.
5. Лист превью: 12 ключевых поз (idle, walk, run, dig, pick_up, sleep, climb, hit, death, zombie_walk, zombie_attack,
   mutant_swiping) на `body_m_rig` — `renders/_review/anims_2026-10-12.jpg`.
6. Отчёт, строка в LOG, коммит и пуш в `main`.

## Имена (файл на Диске → имя действия)

| Файл | Имя | Что это |
|---|---|---|
| Idle / Idle (1) | `idle` (тот, что меньше — без скина) | стоит |
| Unarmed Idle Looking Ver. 2 | `idle_look` | оглядывается |
| Walking / Walking (1) / (2) | `walk`, `walk_b`, `walk_c` | идёт |
| Walk Forward Arc Right | `walk_turn` | идёт с поворотом |
| Jogging | `jog` | бежит трусцой |
| Fast Run | `run` | бежит |
| Strafe | `strafe` | шаг вбок |
| Crouched Sneaking Left | `sneak` | крадётся |
| Crouch To Stand | `crouch_to_stand` | встаёт с корточек |
| Standing Up | `stand_up` | встаёт с пола |
| Kneeling Down | `kneel` | становится на колени (пленник) |
| Crawling | `crawl` | ползёт |
| Picking Up Object | `pick_up` | поднимает |
| Unarmed Grab Torch From Floor | `pick_up_floor` | хватает с пола |
| Pick Fruit | `harvest` | собирает урожай |
| Carrying Turn | `carry_turn` | разворот с ношей |
| Digging | `dig` | копает |
| Working On Device | `work_table` | работает за верстаком |
| Bartending | `work_counter` (второй файл — `work_counter_b`) | работает за стойкой / готовит |
| Looking Through Files Low | `search_low` | роется внизу |
| Rummaging | `search` | обыскивает |
| Open Door Outwards | `open_door` | открывает дверь |
| Opening | `open_box` | открывает ящик |
| Push | `push` | толкает |
| Drinking | `drink` | пьёт |
| Sleeping Idle | `sleep` | спит |
| Sitting Talking | `sit_talk` | сидит, говорит |
| Sitting Rubbing Arm | `sit_injured` | сидит, держится за руку |
| Talking / Talking (1) | `talk`, `talk_b` | говорит |
| Taunt | `taunt` | дразнит (рейдеры) |
| Climbing Ladder | `climb` | лезет по стремянке |
| Climbing Down | `climb_down` | спускается |
| Climbing | `climb_wall` | лезет по стене |
| Freehang Climb | `hang_climb` | висит, лезет |
| Jump / Jumping Down | `jump`, `jump_down` | прыгает |
| Swimming / Floating | `swim`, `float` | плывёт, держится на воде |
| Injured Walk / (1) / Injured Walking | `injured_walk`, `injured_walk_b`, `injured_walk_c` | хромает |
| Injured Run | `injured_run` | бежит раненый |
| Head Hit / Rib Hit | `hit_head`, `hit` | получил удар |
| Standing React Large From Front | `hit_big` | сильный удар |
| Dying / Standing Death Left 01 | `death`, `death_b` | умирает |
| Illegal Elbow Punch | `punch` | удар локтем |
| Punching Bag | `punch_combo` | серия ударов |
| Standing Melee Attack Downward | `melee` | удар сверху (бита, топор, молоток) |
| Double Dagger Stab | `stab` | удар ножом |
| Shooting Gun | `pistol_shoot` | стреляет |
| Gunplay | `gunplay` | стрельба в движении |
| Walk With Rifle | `rifle_walk` | идёт с винтовкой |
| Shooting Arrow | `bow_shoot` | стреляет из лука |
| Entry | `entry` | (посмотреть, что это; записать в отчёт) |
| Zombie Neck Bite | `zombie_neck_bite` | зомби кусает в шею |
| Scary Zombie Pack: zombie idle / walk / run / attack / biting / biting (2) / crawl / running crawl / death / dying / scream / neck bite | `zombie_idle`, `zombie_walk`, `zombie_run`, `zombie_attack`, `zombie_bite`, `zombie_bite_b`, `zombie_crawl`, `zombie_crawl_run`, `zombie_death`, `zombie_dying`, `zombie_scream`, (neck bite — уже есть) | зомби |
| Creature NPC Pack: mutant idle / breathing idle / walking / run / swiping / jumping / dying / flexing muscles / left, right turn 45 | `mutant_idle`, `mutant_idle_b`, `mutant_walk`, `mutant_run`, `mutant_swipe`, `mutant_jump`, `mutant_death`, `mutant_roar`, `mutant_turn_l`, `mutant_turn_r` | громилы-мутанты |
| Action Adventure Pack: idle … idle (5), walking, running, run to stop, crouched sneaking left / right, left / right cover sneak, stand to cover, cover to stand, falling idle, falling to roll, hard landing, jumping up, left / right turn | `aa_idle_1…6`, `aa_walk`, `aa_run`, `run_stop`, `sneak_l`, `sneak_r`, `cover_sneak_l`, `cover_sneak_r`, `to_cover`, `from_cover`, `fall`, `fall_roll`, `land_hard`, `jump_up`, `turn_l`, `turn_r` | запасные и укрытия |

`X Bot.fbx` в наборах — модель-манекен Mixamo, не анимация (не брать).

**Ещё нет (автор докачает):** `eat`, `mine` (удар киркой), `surrender`, `throw`, `rifle_idle`, `rifle_shoot`, `sit` (обычный).
Часть есть в бесплатном наборе игры `godot/assets/animations/ual1_standard.glb` (сидит, перезаряжает, чинит на коленях…).
