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

**7. Ест** — `anim_eat.glb` · повтор
```
Character sits and eats from a bowl held in one hand, bringing a spoon to the mouth with the other hand, chewing, seamless loop.
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

## Потом (по желанию автора)

Работа: за верстаком, шьёт, копает лопатой, поливает и сажает, несёт ящик, поднимает с пола, лезет по лестнице,
открывает дверь, пульт / рация. Бой: выстрел из пистолета и ружья, перезарядка, прицел, получает удар, падает (смерть),
уворачивается. Состояния: хромает, болен, перевязывает себя, испуган, устал, радуется, грустит. Общение: говорит,
машет рукой, торгуется. Зомби и животные — свои (ходьба, бег, атака, удар, смерть).
