# Персонажи: одно тело, сменная одежда, общие анимации

**Готовые запросы целиком — в конце файла** (раздел «Готовые запросы»): копировать и вставлять по очереди.

Решение автора (2026-10-10): у всех людей **одни анимации** (ходьба, бег, копать, есть, спать, драться…), а внешность
разная: одежда, прическа, борода, головной убор, маска, рюкзак, оружие и вещи в руках, ранения.

## Как это устроено

| Часть | Что это | Риг | Как в игре |
|---|---|---|---|
| **1. Тело в одежде** | Одно базовое тело → 8–10 комплектов одежды. **Та же фигура, рост, поза** — меняется только одежда | Да: Tripo → Риг → **Гуманоид**, пресет **Mixamo** | Меняется весь комплект; цвет одежды игра перекрашивает |
| **2. Надеваемое** | Прически, бороды, шапки, каски, маски, рюкзаки, повязки | Нет | Игра крепит к кости: голова / спина / рука |
| **3. В руках** | Оружие и предметы — уже есть в плане объектов (`TRIPO_OBJECTS.md`) | Нет | В правую / левую руку |
| **4. Ранения** | Бинты (надеваемое), кровь, хромота | — | Игра: пятна, повязка, анимация «хромать» |

Почему так: если у всех **одинаковый скелет Mixamo и одинаковые пропорции**, любая анимация подходит любому
персонажу. Одежда, которая гнётся вместе с телом, — часть тела (комплект). Всё твёрдое (каска, рюкзак, топор) —
отдельная модель, её не нужно ригать.

## Шаг 1. Базовое тело (2 шт.: мужчина и женщина)

Образец — **картинка кровати-образца** (как для объектов), ✏️ → запрос → картинка → «Создать».
Важно: **T-поза** (руки в стороны), вид спереди, лысый, без бороды, **в нижнем белье и босиком** — вся одежда и обувь
потом в комплектах.

**`body_base_male.glb`:**
```
Replace the bed with a full body adult man character standing in a strict T-pose, arms straight to the sides, legs slightly apart, front view, average athletic build, bald head, no beard, neutral calm face, wearing only plain grey boxer briefs, barefoot, no accessories. Keep exactly the same art style, level of detail, lighting and dark background as the original image. Single character, no text.
```

**`body_base_female.glb`:**
```
Replace the bed with a full body adult woman character standing in a strict T-pose, arms straight to the sides, legs slightly apart, front view, average athletic build, very short hair tied back, neutral calm face, wearing only a plain grey sports top and plain grey shorts underwear, barefoot, no accessories. Keep exactly the same art style, level of detail, lighting and dark background as the original image. Single character, no text.
```

## Шаг 2. Комплекты одежды (с ригом)

Образец — **картинка базового тела** (мужчины или женщины), ✏️ → запрос → «Создать» → **Риг: Гуманоид, Mixamo** →
Экспорт GLB **с ригом**. Общий конец каждого запроса:
```
Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

| Файл (мужчина / женщина: `_m` / `_f`) | Кто | Начало запроса (+ общий конец) |
|---|---|---|
| `outfit_jumpsuit_m.glb` | выживший из убежища | `Replace the clothes of the character with a worn work jumpsuit with rolled sleeves, a utility belt with pouches and sturdy boots.` |
| `outfit_casual_m.glb` | обычный горожанин | `Replace the clothes of the character with a worn hooded sweatshirt, blue jeans and sneakers.` |
| `outfit_jacket_m.glb` | бродяга | `Replace the clothes of the character with a worn leather jacket over a t-shirt, cargo trousers and boots.` |
| `outfit_military_m.glb` | военный | `Replace the clothes of the character with an old military uniform: camouflage jacket, cargo trousers, knee pads and combat boots.` |
| `outfit_raider_m.glb` | рейдер | `Replace the clothes of the character with raider clothes: torn dark leather jacket with metal spikes on the shoulders, ragged trousers, heavy boots, straps and belts.` |
| `outfit_doctor_m.glb` | медик | `Replace the clothes of the character with a dirty white medical coat over simple clothes and comfortable shoes.` |
| `outfit_worker_m.glb` | рабочий | `Replace the clothes of the character with work overalls with suspenders over a plaid shirt and work boots.` |
| `outfit_winter_m.glb` | зима | `Replace the clothes of the character with a thick padded winter coat, warm trousers and fur boots.` |
| `outfit_trader_m.glb` | торговец | `Replace the clothes of the character with a long patched poncho over layered clothes, wide trousers and wrapped boots.` |
| `outfit_rags_m.glb` | оборванец | `Replace the clothes of the character with torn dirty rags, a ragged shirt and trousers, worn-out shoes.` |

Женские — те же запросы на **женском** базовом теле (`outfit_jumpsuit_f.glb` …). Можно начать с 4 мужских + 4 женских.

## Шаг 3. Надеваемое (без рига)

Образец — **картинка кровати-образца**, как для объектов. Общий конец (как в `TRIPO_OBJECTS.md`):
```
Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**Прически и бороды** (только волосы, без головы — игра надевает на голову):

| Файл | Начало запроса |
|---|---|
| `hair_short.glb` | `Replace the bed with a short messy men's hairstyle shaped as a hair cap only, no head, no face, hollow inside.` |
| `hair_long.glb` | `Replace the bed with a long shoulder-length hairstyle shaped as a hair piece only, no head, no face, hollow inside.` |
| `hair_ponytail.glb` | `Replace the bed with a hairstyle with a ponytail shaped as a hair piece only, no head, no face, hollow inside.` |
| `hair_mohawk.glb` | `Replace the bed with a punk mohawk hairstyle shaped as a hair piece only, no head, no face, hollow inside.` |
| `beard_full.glb` | `Replace the bed with a full thick beard with a moustache only, no face, no head, hollow back side.` |
| `beard_stubble.glb` | `Replace the bed with a short stubble beard and moustache only, no face, no head, hollow back side.` |

**Головные уборы и маски:**

| Файл | Начало запроса |
|---|---|
| `hat_beanie.glb` | `Replace the bed with a knitted beanie hat only, no head, hollow inside.` |
| `hat_cap.glb` | `Replace the bed with a worn baseball cap only, no head, hollow inside.` |
| `hat_helmet_military.glb` | `Replace the bed with an old military helmet only, no head, hollow inside.` |
| `hat_hood.glb` | `Replace the bed with a cloth hood only, no head, hollow inside.` |
| `hat_cowboy.glb` | `Replace the bed with a worn wide-brimmed hat only, no head, hollow inside.` |
| `mask_bandana.glb` | `Replace the bed with a cloth bandana face mask covering the nose and mouth only, no face, hollow back side.` |
| `mask_respirator.glb` | `Replace the bed with a half-face respirator mask with two filters only, no face, hollow back side.` |
| `glasses_goggles.glb` | `Replace the bed with old protective goggles with an elastic strap only, no head.` |

Противогаз (`mask_gas`) уже есть в объектах.

**На тело и ранения:**

| Файл | Начало запроса |
|---|---|
| `back_backpack_big.glb` | `Replace the bed with a big hiking backpack with a rolled sleeping bag on top, back view straps visible.` (малый рюкзак — `backpack` из объектов) |
| `back_quiver.glb` | `Replace the bed with a leather quiver with arrows for the back.` |
| `bandage_head.glb` | `Replace the bed with a white cloth bandage wrapped around a head shape only, no head, hollow inside, a small red stain.` |
| `bandage_arm.glb` | `Replace the bed with a white cloth bandage wrapped as a short tube for an arm, hollow inside, a small red stain.` |
| `sling_arm.glb` | `Replace the bed with a cloth arm sling, hollow, no arm.` |

## Шаг 4. Персонажи «одной моделью» (уже есть)

Рейдер, торговец, зомби, животные из первой пачки — пока **целиком** (риг: люди и зомби — «Гуманоид / Mixamo»,
животные — «Другое»). Позже людей можно собрать из комплектов.

## Куда класть

Google Диск → **«13 Персонажи и существа»**. Имена — как в таблицах. Модели с ригом — экспорт **GLB с ригом**
(без анимаций, только скелет).

## Анимации (потом, одним заданием)

Нужны (для скелета Mixamo — общие на всех): стоять, идти, бежать, идти с грузом, хромать, копать, рубить, строить
(молоток), чинить, искать в ящике, поднять с пола, есть, пить, сидеть, спать (лёжа), лезть по лестнице, удар рукой,
удар оружием, выстрел из пистолета, выстрел из ружья, получить удар, упасть (смерть).
Источник — библиотека Mixamo (бесплатно) или «Анимация» в Tripo; чат игры подключит их ко всем персонажам сразу.

## Обработка (второй чат)

- Тело в одежде: **не облегчать сильно и не трогать кости** (риг Mixamo сохранить), ≤ 15 000 треугольников, рост 1,8 м
  (женщина 1,7 м), стопы в Z = 0, перед к −Y, текстуры 1024 → `export/outfit_<…>_idle.glb`.
- Надеваемое: размер под голову / спину взрослого (шапка ≈ 22 × 15 см, рюкзак ≈ 40 × 55 см), ≤ 2 000 треугольников,
  точка опоры: прическа / шапка — в центре головы снизу; борода / маска — у лица; рюкзак — у спины.

---

## Готовые запросы — копировать целиком

Один серый блок = один запрос. Над блоком: номер, кто это, **имя файла** и **какую картинку взять образцом**.

### А. Базовое тело (образец — картинка кровати-образца)

**1. Базовое тело — мужчина** → `body_base_male.glb`
```
Replace the bed with a full body adult man character standing in a strict T-pose, arms straight to the sides, legs slightly apart, front view, average athletic build, bald head, no beard, neutral calm face, wearing only plain grey boxer briefs, barefoot, no accessories. Keep exactly the same art style, level of detail, lighting and dark background as the original image. Single character, no text.
```

**2. Базовое тело — женщина** → `body_base_female.glb`
```
Replace the bed with a full body adult woman character standing in a strict T-pose, arms straight to the sides, legs slightly apart, front view, average athletic build, very short hair tied back, neutral calm face, wearing only a plain grey sports top and plain grey shorts underwear, barefoot, no accessories. Keep exactly the same art style, level of detail, lighting and dark background as the original image. Single character, no text.
```

### Б. Одежда — мужчина (образец — картинка мужского базового тела; потом Риг: Гуманоид, Mixamo)

**3. выживший из убежища (мужчина)** → `outfit_jumpsuit_m.glb`
```
Replace the clothes of the character with a worn work jumpsuit with rolled sleeves, a utility belt with pouches and sturdy boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**4. обычный горожанин (мужчина)** → `outfit_casual_m.glb`
```
Replace the clothes of the character with a worn hooded sweatshirt, blue jeans and sneakers. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**5. бродяга (мужчина)** → `outfit_jacket_m.glb`
```
Replace the clothes of the character with a worn leather jacket over a t-shirt, cargo trousers and boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**6. военный (мужчина)** → `outfit_military_m.glb`
```
Replace the clothes of the character with an old military uniform: camouflage jacket, cargo trousers, knee pads and combat boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**7. рейдер (мужчина)** → `outfit_raider_m.glb`
```
Replace the clothes of the character with raider clothes: torn dark leather jacket with metal spikes on the shoulders, ragged trousers, heavy boots, straps and belts. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**8. медик (мужчина)** → `outfit_doctor_m.glb`
```
Replace the clothes of the character with a dirty white medical coat over simple clothes and comfortable shoes. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**9. рабочий (мужчина)** → `outfit_worker_m.glb`
```
Replace the clothes of the character with work overalls with suspenders over a plaid shirt and work boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**10. зима (мужчина)** → `outfit_winter_m.glb`
```
Replace the clothes of the character with a thick padded winter coat, warm trousers and fur boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**11. торговец (мужчина)** → `outfit_trader_m.glb`
```
Replace the clothes of the character with a long patched poncho over layered clothes, wide trousers and wrapped boots. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**12. оборванец (мужчина)** → `outfit_rags_m.glb`
```
Replace the clothes of the character with torn dirty rags, a ragged shirt and trousers, worn-out shoes. Keep exactly the same body, proportions, height, face, bald head, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

### В. Одежда — женщина (образец — картинка женского базового тела; потом Риг: Гуманоид, Mixamo)

**13. выживший из убежища (женщина)** → `outfit_jumpsuit_f.glb`
```
Replace the clothes of the character with a worn work jumpsuit with rolled sleeves, a utility belt with pouches and sturdy boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**14. обычный горожанин (женщина)** → `outfit_casual_f.glb`
```
Replace the clothes of the character with a worn hooded sweatshirt, blue jeans and sneakers. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**15. бродяга (женщина)** → `outfit_jacket_f.glb`
```
Replace the clothes of the character with a worn leather jacket over a t-shirt, cargo trousers and boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**16. военный (женщина)** → `outfit_military_f.glb`
```
Replace the clothes of the character with an old military uniform: camouflage jacket, cargo trousers, knee pads and combat boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**17. рейдер (женщина)** → `outfit_raider_f.glb`
```
Replace the clothes of the character with raider clothes: torn dark leather jacket with metal spikes on the shoulders, ragged trousers, heavy boots, straps and belts. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**18. медик (женщина)** → `outfit_doctor_f.glb`
```
Replace the clothes of the character with a dirty white medical coat over simple clothes and comfortable shoes. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**19. рабочий (женщина)** → `outfit_worker_f.glb`
```
Replace the clothes of the character with work overalls with suspenders over a plaid shirt and work boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**20. зима (женщина)** → `outfit_winter_f.glb`
```
Replace the clothes of the character with a thick padded winter coat, warm trousers and fur boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**21. торговец (женщина)** → `outfit_trader_f.glb`
```
Replace the clothes of the character with a long patched poncho over layered clothes, wide trousers and wrapped boots. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

**22. оборванец (женщина)** → `outfit_rags_f.glb`
```
Replace the clothes of the character with torn dirty rags, a ragged shirt and trousers, worn-out shoes. Keep exactly the same body, proportions, height, face, short hair tied back, T-pose, camera angle, art style, lighting and dark background as the original image. Only the clothes change. No hat, no hair, no backpack, nothing in the hands. Single character, no text.
```

### Г. Надеваемое (образец — картинка кровати-образца; без рига)

**23.** → `hair_short.glb`
```
Replace the bed with a short messy men's hairstyle shaped as a hair cap only, no head, no face, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**24.** → `hair_long.glb`
```
Replace the bed with a long shoulder-length hairstyle shaped as a hair piece only, no head, no face, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**25.** → `hair_ponytail.glb`
```
Replace the bed with a hairstyle with a ponytail shaped as a hair piece only, no head, no face, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**26.** → `hair_mohawk.glb`
```
Replace the bed with a punk mohawk hairstyle shaped as a hair piece only, no head, no face, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**27.** → `beard_full.glb`
```
Replace the bed with a full thick beard with a moustache only, no face, no head, hollow back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**28.** → `beard_stubble.glb`
```
Replace the bed with a short stubble beard and moustache only, no face, no head, hollow back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**29.** → `hat_beanie.glb`
```
Replace the bed with a knitted beanie hat only, no head, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**30.** → `hat_cap.glb`
```
Replace the bed with a worn baseball cap only, no head, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**31.** → `hat_helmet_military.glb`
```
Replace the bed with an old military helmet only, no head, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**32.** → `hat_hood.glb`
```
Replace the bed with a cloth hood only, no head, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**33.** → `hat_cowboy.glb`
```
Replace the bed with a worn wide-brimmed hat only, no head, hollow inside. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**34.** → `mask_bandana.glb`
```
Replace the bed with a cloth bandana face mask covering the nose and mouth only, no face, hollow back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**35.** → `mask_respirator.glb`
```
Replace the bed with a half-face respirator mask with two filters only, no face, hollow back side. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**36.** → `glasses_goggles.glb`
```
Replace the bed with old protective goggles with an elastic strap only, no head. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**37.** → `back_backpack_big.glb`
```
Replace the bed with a big hiking backpack with a rolled sleeping bag on top, back view straps visible. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**38.** → `back_quiver.glb`
```
Replace the bed with a leather quiver with arrows for the back. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**39.** → `bandage_head.glb`
```
Replace the bed with a white cloth bandage wrapped around a head shape only, no head, hollow inside, a small red stain. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**40.** → `bandage_arm.glb`
```
Replace the bed with a white cloth bandage wrapped as a short tube for an arm, hollow inside, a small red stain. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```

**41.** → `sling_arm.glb`
```
Replace the bed with a cloth arm sling, hollow, no arm. Keep exactly the same art style, level of detail, lighting, camera angle and dark background as the original image. Use the object's own natural colors and materials, not the colors of the bed; add rust and wear only where it makes sense for this object. Single object, no text.
```
