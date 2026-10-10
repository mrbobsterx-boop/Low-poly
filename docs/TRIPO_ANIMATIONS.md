# Анимации персонажей — запросы для Tripo

Решение автора (2026-10-10): у всех людей **одни анимации** на скелете Mixamo (`docs/TRIPO_CHARACTERS.md`) —
любая анимация подходит любому персонажу.

## Как делать

1. Tripo → модель персонажа с ригом (**Гуманоид, пресет Mixamo**) → **Анимация** → вставить запрос из списка (серый блок)
   целиком, по-английски.
2. Посмотреть результат. Не похоже — повторить.
3. Скачать **GLB с анимацией**, назвать **как в списке** (`anim_<имя>.glb`), положить на Google Диск в
   **«13 Персонажи и существа»** (можно подпапка «Анимации»).

**Слова в запросах:** *in place* — персонаж не уезжает с места (двигает его игра); *seamless loop* — движение повторяется
без рывка. Где их нет — действие с началом и концом (лечь, снять рюкзак), играется один раз.

---

## А. Основа (без неё не обойтись)

**1. Стоит спокойно** — `anim_idle.glb` · повтор
```
Character stands relaxed, breathing calmly, small weight shifts from one foot to the other, occasionally looks around, seamless loop, in place.
```

**2. Идёт** — `anim_walk.glb` · повтор
```
Character walks forward at a normal relaxed pace, natural arm swing, seamless loop, in place.
```

**3. Бежит** — `anim_run.glb` · повтор
```
Character runs forward at a fast steady pace, arms swinging, leaning slightly forward, seamless loop, in place.
```

**4. Сидит на стуле** — `anim_sit_chair.glb` · повтор
```
Character sits on a chair, back slightly leaning, hands resting on the knees, calm breathing, small head movements, seamless loop.
```

**5. Спит лёжа** — `anim_sleep.glb` · повтор
```
Character lies on the back sleeping, chest slowly rising and falling, occasionally shifts slightly, seamless loop.
```

**6. Поворачивается** — `anim_turn.glb` · один раз
```
Character standing turns around 180 degrees on the spot with small steps and returns to a relaxed stance.
```

---

## Б. Быт

**7. Ест сидя** — `anim_eat.glb` · повтор
```
Character sits and eats from a bowl held in one hand, bringing a spoon to the mouth with the other hand, chewing, seamless loop.
```

**7б. Ест стоя** — `anim_eat_standing.glb` · повтор
```
Character stands and eats, holding a piece of food in one hand, taking bites and chewing, the other hand relaxed at the side, small weight shifts, seamless loop, in place.
```

**8. Пьёт из бутылки** — `anim_drink.glb` · один раз
```
Character standing raises a bottle to the mouth, tilts the head back and drinks a few gulps, then lowers the bottle and wipes the mouth with the back of the hand.
```

**9. Готовит у плиты** — `anim_cook.glb` · повтор
```
Character stands at a stove and stirs food in a pot with a spoon, occasionally adds something with the other hand and leans in to smell it, seamless loop.
```

**10. Умывается** — `anim_wash.glb` · повтор
```
Character leans over a sink, scoops water with both hands and splashes it on the face, rubs the face, seamless loop.
```

**11. Читает** — `anim_read.glb` · повтор
```
Character sits holding an open book or note with both hands, reading, eyes moving along the lines, occasionally turns a page, seamless loop.
```

**12. Отдыхает у костра** — `anim_rest_campfire.glb` · повтор
```
Character sits on the ground with legs crossed, leaning forward and holding both hands out toward a fire to warm them, rubbing the hands from time to time, seamless loop.
```

---

## В. Действия (список автора)

**13. Снял рюкзак и смотрит в него** — `anim_backpack_open.glb` · один раз
```
Character takes off a backpack from the shoulders, puts it on the ground in front, kneels and rummages through it with both hands, looking inside. In place.
```

**14. Ползёт по полу** — `anim_crawl.glb` · повтор
```
Character crawls forward on the floor on hands and knees, slow steady pace, seamless loop, in place.
```

**15. Едет за рулём** — `anim_drive.glb` · повтор
```
Character sits and drives a car, both hands on the steering wheel, small turns of the wheel left and right, looking forward, seamless loop.
```

**16. Едет на велосипеде** — `anim_bike.glb` · повтор
```
Character sits on a bicycle and pedals at a steady pace, hands on the handlebars, slight body sway, seamless loop, in place.
```

**17. Бежит на беговой дорожке** — `anim_treadmill.glb` · повтор
```
Character runs at a steady medium pace on a treadmill, arms swinging, breathing hard, seamless loop, in place.
```

**18. Ремонтирует** — `anim_repair.glb` · повтор
```
Character stands at a table and repairs a device with a wrench and a screwdriver, small precise hand movements, leaning slightly forward, seamless loop.
```

**19. Бьёт двуручным оружием** — `anim_attack_twohand.glb` · один раз
```
Character swings a heavy two-handed weapon from over the shoulder down in a powerful strike, then returns to a ready stance.
```

**20. Бьёт одноручным оружием** — `anim_attack_onehand.glb` · один раз
```
Character makes a fast one-handed swing with a short melee weapon from right to left, then returns to a ready stance.
```

**21. Ложится на кровать** — `anim_lie_down.glb` · один раз
```
Character sits down on the edge of a bed, then lies down on the back, settles and stays still.
```

**22. Светит фонариком** — `anim_flashlight.glb` · повтор
```
Character walks slowly holding a flashlight in one hand at chest height, pointing it forward and slowly sweeping left and right, seamless loop.
```

**23. Рубит дерево** — `anim_chop.glb` · повтор
```
Character chops a tree with an axe held in both hands, side swings into the trunk, steady rhythm, seamless loop, in place.
```

**24. Обыскивает ящики** — `anim_search_box.glb` · повтор
```
Character bends over an open box on the floor and searches through it with both hands, picking items up, looking at them and putting them back, seamless loop.
```

**25. Присел и взламывает замок** — `anim_lockpick.glb` · повтор
```
Character crouches in front of a door and picks a lock with two small tools, careful small wrist movements, looking closely at the lock, seamless loop.
```

**26. Крадётся** — `anim_sneak.glb` · повтор
```
Character sneaks forward in a low crouch, slow careful steps, arms slightly out for balance, seamless loop, in place.
```

**27. Разделывает животное** — `anim_butcher.glb` · повтор
```
Character kneels on the ground and butchers an animal carcass with a knife, cutting motions with one hand and holding with the other, seamless loop.
```

**28. Обыскивает труп** — `anim_search_body.glb` · повтор
```
Character kneels next to a body lying on the ground and searches its pockets with both hands, looking around nervously from time to time, seamless loop.
```

**29. Обыскивает шкаф** — `anim_search_cabinet.glb` · повтор
```
Character stands in front of a tall cabinet, opens it and searches the shelves with both hands at chest and head height, seamless loop.
```

**30. Долбит киркой** — `anim_mine.glb` · повтор
```
Character strikes the ground in front with a pickaxe held in both hands, overhead swings, steady rhythm, seamless loop, in place.
```

**31. Кормит животное** — `anim_feed_animal.glb` · повтор
```
Character crouches and holds out food in one open hand toward a small animal on the ground, then puts it down gently, seamless loop.
```

---

## Г. Работа

**32. Работает за верстаком** — `anim_workbench.glb` · повтор
```
Character stands at a workbench and works with both hands: hammering lightly, then adjusting a part, leaning slightly over the table, seamless loop, in place.
```

**33. Шьёт** — `anim_sew.glb` · повтор
```
Character sits at a table and sews by hand, pulling a needle and thread through fabric with small careful motions, seamless loop.
```

**34. Копает лопатой** — `anim_dig.glb` · повтор
```
Character digs the ground with a shovel: pushes it in with the foot, lifts the soil and throws it to the side, steady rhythm, seamless loop, in place.
```

**35. Поливает и сажает** — `anim_plant.glb` · повтор
```
Character kneels at a garden bed, makes a small hole in the soil with the hand, puts a seed in, covers it, then picks up a watering can and waters it, seamless loop.
```

**36. Несёт ящик** — `anim_carry_box.glb` · повтор
```
Character walks forward carrying a heavy box in front of the chest with both arms, leaning back slightly from the weight, seamless loop, in place.
```

**37. Поднимает с пола** — `anim_pick_up.glb` · один раз
```
Character bends down, picks up a small item from the floor with one hand, straightens up and looks at it.
```

**38. Лезет по лестнице** — `anim_climb_ladder.glb` · повтор
```
Character climbs up a vertical ladder, hands and feet moving alternately on the rungs, seamless loop, in place.
```

**39. Открывает дверь** — `anim_open_door.glb` · один раз
```
Character reaches out, grabs a door handle, turns it and pulls the door open, then steps forward.
```

**40. Пульт / рация** — `anim_radio.glb` · повтор
```
Character stands at a control panel with a radio, presses buttons and turns knobs with one hand, then raises a handset to the mouth and speaks, seamless loop.
```

---

## Д. Бой

**41. Стреляет из пистолета** — `anim_shoot_pistol.glb` · один раз
```
Character holds a pistol in both hands at arm's length, aims forward and fires one shot with a small recoil, then returns to the aiming pose.
```

**42. Стреляет из ружья** — `anim_shoot_rifle.glb` · один раз
```
Character holds a rifle at the shoulder, aims forward and fires one shot with a strong recoil, then returns to the aiming pose.
```

**43. Перезаряжает** — `anim_reload.glb` · один раз
```
Character holding a gun takes out the empty magazine, inserts a new one from the belt and racks the gun, then returns to a ready stance.
```

**44. Целится** — `anim_aim.glb` · повтор
```
Character stands holding a gun raised and aimed forward, steady, small breathing movements, seamless loop, in place.
```

**45. Получает удар** — `anim_hit.glb` · один раз
```
Character gets hit in the chest, staggers back one step, bends slightly in pain, then recovers to a standing stance.
```

**46. Падает (смерть)** — `anim_death.glb` · один раз
```
Character gets a fatal hit, knees give way, falls backward onto the ground and lies still.
```

**47. Уворачивается** — `anim_dodge.glb` · один раз
```
Character quickly dodges to the side with a short step and leans the body away, then returns to a ready stance.
```

---

## Е. Состояния

**48. Хромает** — `anim_limp.glb` · повтор
```
Character walks forward limping on the right leg, putting little weight on it, one hand on the thigh, seamless loop, in place.
```

**49. Болен** — `anim_sick.glb` · повтор
```
Character stands hunched, coughing hard, one hand over the mouth and the other on the stomach, swaying slightly, seamless loop, in place.
```

**50. Перевязывает себя** — `anim_bandage.glb` · один раз
```
Character sits on the ground and wraps a bandage around the own forearm with the other hand, then ties it.
```

**51. Испуган** — `anim_scared.glb` · повтор
```
Character stands frightened, shoulders raised, looking around quickly, stepping back a little and hands half raised in front, seamless loop, in place.
```

**52. Устал** — `anim_tired.glb` · повтор
```
Character stands bent forward with hands on the knees, breathing heavily, head down, seamless loop, in place.
```

---

## Потом (по желанию автора)

Состояния: радуется, грустит. Общение: говорит, машет рукой, торгуется. Зомби и животные — свои
(ходьба, бег, атака, удар, смерть).
