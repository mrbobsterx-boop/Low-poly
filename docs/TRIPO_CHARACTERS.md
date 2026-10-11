# Персонажи, одежда, надеваемое, животные — что делать в Tripo (новый стиль, 2026-10-11)

**Референс автора** — стилизованный low poly выживший: рубленые грани, плоская заливка, простое лицо (глаза-чёрточки,
без рта), тёплый свет, тёмный фон, кровь пятнами. Картинку-референс даёшь в Tripo **как образец стиля** к каждому запросу. Референсы лежат здесь:
[мужчина](ref/character_ref_m.jpg), [женщина](ref/character_ref_f.jpg).
(Старый план под прежний стиль — в истории git, этот его заменяет.)

## Как это устроено в игре (коротко)

| Что | Риг | Как в игре |
|---|---|---|
| **А. Тело** (лысое, в белье) | Да: Риг → **Гуманоид**, пресет **Mixamo** | основа для всех людей и зомби, одни анимации на всех |
| **Б. Комплект одежды на теле** (рубашка + штаны + обувь — одной моделью) | Да, как тело | внешность персонажа; цвет игра может перекрашивать |
| **В. Надеваемое** (причёски, шапки, маски, рюкзаки, бинты) | **Нет** | игра крепит к кости: голова / спина / рука / бедро |
| **Г. В руках** (оружие, инструменты, вещи) | Нет | в правую / левую руку |
| **Д. Зомби, мутанты, люди-NPC целиком** | Да, Гуманоид Mixamo | те же анимации, что у людей |
| **Е. Животные** | Риг «четвероногое», если Tripo даёт; нет — без рига | анимации — свои |

**Главное правило:** у всех людей и зомби — **одна фигура, рост и поза** (как у тела А1 / А2). Тогда любая анимация
подходит любому, а причёски и шапки садятся на любую голову.

## Как делать — по порядку

1. Сначала **А1 и А2** (тела) → пришли, проверю рост и пропорции.
2. Потом **Б** — образец: картинка **твоего тела А1** (мужское) или **А2** (женское) + референс стиля.
3. **В, Г, Е** — образец: референс стиля. Без рига.
4. Скачать GLB (с ригом — «GLB с ригом»), **назвать как в списке**, положить на Google Диск в папку
   **«13 Персонажи и существа»** (подпапки можно любые). Я заберу и обработаю.

**Хвост ко всем запросам людей (А, Б, Д)** — копировать в конец:
```
Stylized low poly 3D character in exactly the same art style as the reference image: faceted flat-shaded surfaces, simplified blocky face with small dark eyes and no mouth, warm soft lighting, dark background. Full body, standing in a strict T-pose, arms straight to the sides, legs slightly apart, front view, same body proportions and height as the reference. Single character, no weapon in hands, no text.
```

**Хвост к вещам (В, Г, Е)**:
```
Stylized low poly 3D model in exactly the same art style as the reference image: faceted flat-shaded surfaces, simple shapes, warm soft lighting, dark background. Single object, centered, no character, no text.
```

---

## А. Тела (с ригом) — 2 шт.

| № | Файл | Запрос (+ хвост людей) |
|---|---|---|
| А1 | `body_m_bald.glb` | `Adult man, bald head, no hair, no beard, wearing only plain grey boxer briefs, barefoot.` |
| А2 | `body_f_bald.glb` | `Adult woman, bald head, no hair, wearing only a plain grey sports top and grey shorts, barefoot.` |

## Б. Комплекты одежды (с ригом) — лысые, причёска отдельно

Мужские (образец — тело А1):

| № | Файл | Запрос (+ хвост людей) |
|---|---|---|
| Б1 | `outfit_m_flannel.glb` | `Bald man in a red plaid flannel shirt over a white t-shirt, dark jeans, red sneakers.` (как референс) |
| Б2 | `outfit_m_hoodie.glb` | `Bald man in a grey hoodie, cargo pants, worn sneakers.` |
| Б3 | `outfit_m_work.glb` | `Bald man in orange work overalls, heavy work boots, knee pads.` |
| Б4 | `outfit_m_military.glb` | `Bald man in green military uniform, combat pants, combat boots.` |
| Б5 | `outfit_m_raider.glb` | `Bald man raider in a black leather jacket with metal studs, ripped jeans, spiked shoulder pad, boots.` |
| Б6 | `outfit_m_winter.glb` | `Bald man in a thick winter parka, warm pants, snow boots.` |
| Б7 | `outfit_m_doctor.glb` | `Bald man in a dirty white doctor coat over scrubs, sneakers.` |
| Б8 | `outfit_m_trader.glb` | `Bald man trader in a long brown coat with many pockets, scarf, boots.` |
| Б9 | `outfit_m_police.glb` | `Bald man in a dark blue police uniform, utility belt, boots.` |
| Б10 | `outfit_m_suit.glb` | `Bald man in a torn office suit with loose tie, dress shoes.` |

Женские (образец — тело А2):

| № | Файл | Запрос (+ хвост людей) |
|---|---|---|
| Б11 | `outfit_f_punk.glb` | `Bald woman in a cropped dark jacket over a white crop top, ripped grey jeans, red high-top sneakers.` (как референс) |
| Б12 | `outfit_f_hoodie.glb` | `Bald woman in an oversized hoodie, leggings, sneakers.` |
| Б13 | `outfit_f_work.glb` | `Bald woman in mechanic overalls tied at the waist, tank top, work boots.` |
| Б14 | `outfit_f_military.glb` | `Bald woman in military uniform, combat pants, combat boots.` |
| Б15 | `outfit_f_raider.glb` | `Bald woman raider in a studded leather vest, torn pants, boots, arm wraps.` |
| Б16 | `outfit_f_winter.glb` | `Bald woman in a puffy winter jacket, warm pants, snow boots.` |
| Б17 | `outfit_f_doctor.glb` | `Bald woman in a dirty white doctor coat over scrubs, sneakers.` |
| Б18 | `outfit_f_farmer.glb` | `Bald woman in a denim shirt, overalls, rubber boots.` |
| Б19 | `outfit_f_sport.glb` | `Bald woman in a sports jacket, track pants, running shoes.` |
| Б20 | `outfit_f_dress.glb` | `Bald woman in a simple torn summer dress with a cardigan, flat shoes.` |

## В. Надеваемое (без рига) — крепится к голове / спине / руке

Причёски (сидят на лысой голове тела):

| № | Файл | Запрос (+ хвост вещей) |
|---|---|---|
| В1 | `hair_short.glb` | `Short messy brown hair cap for a low poly character head, hair only, no head.` |
| В2 | `hair_buzz.glb` | `Very short buzz cut hair, hair only, no head.` |
| В3 | `hair_dreads.glb` | `Shoulder-length dreadlocks with colorful beads, hair only, no head.` (как референс) |
| В4 | `hair_ponytail.glb` | `Long hair tied in a ponytail, hair only, no head.` |
| В5 | `hair_bun.glb` | `Hair tied in a messy bun, hair only, no head.` |
| В6 | `hair_mohawk.glb` | `Punk mohawk hair, hair only, no head.` |
| В7 | `hair_long.glb` | `Long straight hair to the shoulders, hair only, no head.` |
| В8 | `hair_curly.glb` | `Big curly afro hair, hair only, no head.` |
| В9 | `hair_bob.glb` | `Short bob haircut, hair only, no head.` |
| В10 | `beard_full.glb` | `Full thick beard and moustache, beard only, no head.` |
| В11 | `beard_stubble.glb` | `Short stubble beard, beard only, no head.` |

Головные уборы и маски:

| № | Файл | Запрос (+ хвост вещей) |
|---|---|---|
| В12 | `hat_cap.glb` | `Worn baseball cap with a small headlamp on top.` (как референс) |
| В13 | `hat_beanie.glb` | `Knitted beanie hat.` |
| В14 | `hat_hardhat.glb` | `Yellow construction hard hat.` |
| В15 | `hat_helmet_mil.glb` | `Green military combat helmet.` |
| В16 | `hat_bandana.glb` | `Red bandana tied on the head.` |
| В17 | `hat_cowboy.glb` | `Worn brown cowboy hat.` |
| В18 | `mask_gas.glb` | `Gas mask with round filter.` |
| В19 | `mask_respirator.glb` | `Half-face respirator mask with two filters.` |
| В20 | `mask_hockey.glb` | `White hockey goalie mask with holes.` |
| В21 | `mask_cloth.glb` | `Cloth bandana covering the lower face.` |
| В22 | `mask_welding.glb` | `Welding mask.` |
| В23 | `goggles.glb` | `Ski goggles worn on the forehead.` |
| В24 | `glasses.glb` | `Simple round glasses.` |

Спина, руки, пояс:

| № | Файл | Запрос (+ хвост вещей) |
|---|---|---|
| В25 | `back_backpack_small.glb` | `Small olive backpack with straps and buckles.` (как референс) |
| В26 | `back_backpack_big.glb` | `Large hiking backpack with a rolled sleeping bag on top.` |
| В27 | `back_backpack_mil.glb` | `Military tactical backpack with pouches.` |
| В28 | `back_quiver.glb` | `Quiver with arrows.` |
| В29 | `vest_armor.glb` | `Black bulletproof vest with pouches, vest only, no body.` |
| В30 | `vest_hiviz.glb` | `Orange high-visibility safety vest, vest only, no body.` |
| В31 | `arm_bandage.glb` | `Bloody bandage wrap for a forearm.` |
| В32 | `arm_wristwatch.glb` | `Wristwatch with a leather strap.` |
| В33 | `arm_gloves.glb` | `Pair of fingerless leather gloves.` |
| В34 | `belt_holster.glb` | `Leg holster with strap.` |
| В35 | `belt_pouches.glb` | `Utility belt with pouches.` |

## Г. В руках (без рига)

Уже есть в игре (модели сделаны): бита, мачете, труба, лук, пистолет, дробовик, топор, лом, кирка, лопата, кувалда,
пила, молоток, нож, фонарик, гаечный ключ, отвёртка, паяльник, ведро, котелок. **Новые** (в игре станут объектами —
добавлю их в ОС):

| № | Файл | Запрос (+ хвост вещей) |
|---|---|---|
| Г1 | `weapon_cleaver.glb` | `Bloody meat cleaver with a wooden handle.` (как референс) |
| Г2 | `weapon_bat_nails.glb` | `Wooden baseball bat with nails and wire wrapped around it.` (как референс) |
| Г3 | `weapon_axe_fire.glb` | `Red fire axe.` |
| Г4 | `weapon_spear.glb` | `Makeshift spear: knife taped to a long pole.` |
| Г5 | `weapon_golf.glb` | `Golf club.` |
| Г6 | `weapon_rifle.glb` | `Old hunting rifle with a wooden stock.` |
| Г7 | `weapon_crossbow.glb` | `Simple crossbow.` |
| Г8 | `weapon_molotov.glb` | `Molotov cocktail: glass bottle with a rag.` |
| Г9 | `item_torch.glb` | `Burning wooden torch.` |
| Г10 | `item_flare.glb` | `Red road flare.` |
| Г11 | `item_radio.glb` | `Handheld walkie-talkie radio.` |
| Г12 | `item_bottle.glb` | `Plastic water bottle.` |
| Г13 | `item_can.glb` | `Tin can of food.` |
| Г14 | `item_map.glb` | `Folded paper map.` |
| Г15 | `item_medkit.glb` | `Small red first aid kit.` |
| Г16 | `item_binoculars.glb` | `Binoculars.` |

## Д. Целиком: зомби, мутанты, люди-NPC (с ригом, Гуманоид Mixamo)

Образец — тело А1 / А2 + референс (та же фигура — те же анимации).

| № | Файл | Запрос (+ хвост людей) |
|---|---|---|
| Д1 | `zombie_walker_m.glb` | `Zombie man, grey-green skin, torn flannel shirt and jeans, blood stains, empty white eyes.` |
| Д2 | `zombie_walker_f.glb` | `Zombie woman, grey-green skin, torn clothes, messy hair, blood stains.` |
| Д3 | `zombie_runner.glb` | `Thin fast zombie in torn sports clothes, grey-green skin.` |
| Д4 | `zombie_brute.glb` | `Huge muscular zombie, torn work clothes, swollen arms.` |
| Д5 | `zombie_riot.glb` | `Zombie in riot police armor and cracked helmet.` |
| Д6 | `zombie_hazmat.glb` | `Zombie in a torn yellow hazmat suit.` |
| Д7 | `zombie_doctor.glb` | `Zombie in a bloody doctor coat.` |
| Д8 | `zombie_bloated.glb` | `Bloated fat zombie with swollen green belly.` |
| Д9 | `mutant_crawler.glb` | `Mutant crawler: thin pale creature on all fours, long arms, no legs below the knees.` (без T-позы: на четвереньках) |
| Д10 | `raider_boss.glb` | `Raider leader with a spiked shoulder armor, skull face paint, leather coat.` |
| Д11 | `trader_npc.glb` | `Old trader with a long coat, many bags and pouches, grey beard.` |
| Д12 | `soldier_npc.glb` | `Soldier in full gear: helmet, armor vest, gas mask on the belt.` |

## Е. Животные (риг «четвероногое», если есть; нет — без рига)

| № | Файл | Запрос (+ хвост вещей) |
|---|---|---|
| Е1 | `dog_feral.glb` | `Feral stray dog, thin, dirty brown fur, standing on four legs, side view.` |
| Е2 | `dog_shepherd.glb` | `Friendly German shepherd dog with a red collar, standing, side view.` |
| Е3 | `dog_zombie.glb` | `Zombie dog with torn skin and exposed ribs, standing, side view.` |
| Е4 | `cat.glb` | `Grey tabby cat, standing, side view.` |
| Е5 | `rabbit_wild.glb` | `Wild brown rabbit, sitting, side view.` |
| Е6 | `rat.glb` | `Big grey rat, side view.` |
| Е7 | `crow.glb` | `Black crow standing, side view.` |
| Е8 | `chicken.glb` | `Chicken, side view.` |
| Е9 | `goat.glb` | `Goat with small horns, standing, side view.` |
| Е10 | `deer.glb` | `Deer with antlers, standing, side view.` |
| Е11 | `boar.glb` | `Wild boar with tusks, standing, side view.` |
| Е12 | `wolf.glb` | `Grey wolf, standing, side view.` |

## С чего начать (если мало времени)

**А1, А2** → **Б1, Б11** → **В1, В3, В12, В25** → **Д1** → **Е1**. Это уже даст: мужчину и женщину как на референсе,
причёски и кепку отдельно, зомби и собаку. Пришлёшь — проверю, как садится на тело и анимации, потом остальное.
