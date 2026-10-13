"""Список действий персонажей и анимаций-кандидатов к каждому → export/anim/anim_actions.json (для редактора анимаций
в игре: выбрать действие → посмотреть кандидатов на персонаже → ⭐ закрепить подходящую).

  python3 tools/anim_actions.py

Кандидаты подбираются по словам в именах анимаций из всех наборов (Mixamo — общий, Tripo — у тел со скелетом).
Закреплённые (`pinned`) из прежнего файла сохраняются.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANIM = os.path.join(ROOT, "export", "anim")

# файл анимаций → короткое имя набора; все — на скелете тел Tripo (кости Mixamo), подходят ко всем людям
SOURCES = {
    "mixamo": "anims_mixamo.glb",
    "tripo_m": "body_m_rig_anims.glb",
    "tripo_m_b": "body_m_rig_b_anims.glb",
    "tripo_f": "body_f_rig_anims.glb",
}

# id действия, название, группа, слова для поиска кандидатов (регулярные выражения по имени анимации)
ACTIONS = [
    ("idle", "Стоит", "Основа", [r"^idle$", r"idle_look", r"^aa_idle", r"^wait$", r"look_around", r"stands relaxed"]),
    ("walk", "Идёт", "Основа", [r"^walk(_b|_c)?$", r"^aa_walk$", r"^walk$", r"walks forward at a normal"]),
    ("run", "Бежит", "Основа", [r"^run$", r"^jog$", r"^aa_run$", r"runs forward", r"treadmill"]),
    ("sneak", "Крадётся", "Основа", [r"sneak", r"low crouch"]),
    ("crawl", "Ползёт", "Основа", [r"^crawl$", r"crawls forward"]),
    ("turn", "Поворачивается", "Основа", [r"^turn", r"turns around"]),
    ("climb", "Лезет по лестнице", "Основа", [r"^climb", r"climbs up a vertical", r"hang_climb", r"run_upstairs"]),
    ("jump", "Прыгает", "Основа", [r"^jump", r"jumping", r"land_hard"]),
    ("sit", "Сидит", "Быт", [r"^sit$", r"sits on a chair", r"sit_talk"]),
    ("sleep", "Спит", "Быт", [r"^sleep$", r"lies on the back sleeping", r"ложиться спать"]),
    ("lie_down", "Ложится на кровать", "Быт", [r"sits down on the edge of a bed", r"ложиться"]),
    ("eat", "Ест сидя", "Быт", [r"sits and eats"]),
    ("eat_stand", "Ест стоя", "Быт", [r"stands and eats", r"достает из кормана еду"]),
    ("drink", "Пьёт", "Быт", [r"^drink$", r"raises a bottle"]),
    ("cook", "Готовит", "Быт", [r"stove", r"work_counter"]),
    ("read", "Читает", "Быт", [r"open book"]),
    ("rest_fire", "Греется у костра", "Быт", [r"legs crossed, leaning forward"]),
    ("take_pills", "Принимает таблетки", "Быт", [r"таблетки"]),
    ("backpack", "Снимает рюкзак, смотрит", "Быт", [r"backpack", r"рюкзак"]),
    ("pick_up", "Поднимает с пола", "Работа", [r"^pick_up", r"picks up a small item", r"lift_heavy"]),
    ("carry", "Несёт ящик", "Работа", [r"carrying a heavy box", r"carry_turn", r"^box_0"]),
    ("open_door", "Открывает дверь", "Работа", [r"open_door", r"door handle"]),
    ("open_box", "Открывает ящик / сундук", "Работа", [r"open_box", r"^search$", r"open box on the floor"]),
    ("search_cabinet", "Обыскивает шкаф", "Работа", [r"tall cabinet", r"search_low"]),
    ("search_body", "Обыскивает труп", "Работа", [r"next to a body", r"присел на одно колено"]),
    ("lockpick", "Взламывает замок", "Работа", [r"picks a lock"]),
    ("chop", "Рубит дерево", "Работа", [r"^chop$", r"chops a tree", r"^melee$"]),
    ("mine", "Долбит киркой", "Работа", [r"pickaxe", r"^melee$"]),
    ("dig", "Копает", "Работа", [r"^dig$", r"^shovel$"]),
    ("plant", "Сажает и поливает", "Работа", [r"garden bed", r"harvest"]),
    ("harvest", "Собирает урожай", "Работа", [r"^harvest$"]),
    ("butcher", "Разделывает", "Работа", [r"butchers"]),
    ("feed_animal", "Кормит животное", "Работа", [r"holds out food"]),
    ("work_table", "Работает за верстаком", "Работа", [r"work_table", r"workbench", r"мастерит за столом"]),
    ("repair", "Ремонтирует", "Работа", [r"repairs a device", r"work_table"]),
    ("sew", "Шьёт", "Работа", [r"sews by hand"]),
    ("radio", "Рация / пульт", "Работа", [r"control panel"]),
    ("push", "Толкает", "Работа", [r"^push$"]),
    ("talk", "Говорит", "Общение", [r"^talk", r"talks, natural", r"^agree$"]),
    ("trade", "Торгуется", "Общение", [r"bargains"]),
    ("wave", "Машет рукой", "Общение", [r"wave_goodbye"]),
    ("laugh", "Смеётся", "Общение", [r"laugh"]),
    ("taunt", "Дразнит", "Общение", [r"^taunt$", r"frustrated"]),
    ("attack_melee", "Бьёт (одной рукой)", "Бой", [r"one-handed swing", r"^punch", r"^stab$", r"^slash$", r"front_kick"]),
    ("attack_2h", "Бьёт двуручным", "Бой", [r"two-handed weapon", r"^melee$"]),
    ("shoot_pistol", "Стреляет из пистолета", "Бой", [r"pistol", r"выстрел с пистолета", r"^shoot$", r"^fire$"]),
    ("shoot_rifle", "Стреляет из винтовки", "Бой", [r"rifle at the shoulder", r"gunplay", r"rifle_walk"]),
    ("aim", "Целится", "Бой", [r"raised and aimed"]),
    ("reload", "Перезаряжает", "Бой", [r"magazine"]),
    ("bow", "Стреляет из лука", "Бой", [r"bow_shoot"]),
    ("dodge", "Уворачивается", "Бой", [r"dodges", r"fall_roll"]),
    ("hit", "Получает удар", "Бой", [r"^hit", r"hit_to_"]),
    ("death", "Падает (смерть)", "Бой", [r"^death", r"defeat"]),
    ("flee", "Убегает в страхе", "Состояния", [r"^flee"]),
    ("limp", "Хромает", "Состояния", [r"injured_walk", r"limping"]),
    ("injured_run", "Бежит раненый", "Состояния", [r"injured_run"]),
    ("bandage", "Перевязывается", "Состояния", [r"bandage", r"left forearm out"]),
    ("sick", "Болен", "Состояния", [r"coughing"]),
    ("tired", "Устал", "Состояния", [r"hands on the knees"]),
    ("sit_injured", "Сидит раненый", "Состояния", [r"sit_injured"]),
    ("kneel", "На коленях (пленник)", "Состояния", [r"^kneel$"]),
    ("swim", "Плывёт", "Состояния", [r"^swim$", r"^float$", r"^dive$"]),
    ("zombie_idle", "Зомби — стоит", "Зомби", [r"^zombie_idle", r"^zombie_scream"]),
    ("zombie_walk", "Зомби — идёт", "Зомби", [r"^zombie_walk"]),
    ("zombie_run", "Зомби — бежит", "Зомби", [r"^zombie_run", r"zombie_crawl_run"]),
    ("zombie_crawl", "Зомби — ползёт", "Зомби", [r"^zombie_crawl$"]),
    ("zombie_attack", "Зомби — атакует", "Зомби", [r"^zombie_attack", r"zombie_bite", r"zombie_neck_bite"]),
    ("zombie_death", "Зомби — умирает", "Зомби", [r"zombie_death", r"zombie_dying"]),
    ("mutant_idle", "Мутант — стоит", "Мутант", [r"^mutant_idle", r"mutant_roar"]),
    ("mutant_walk", "Мутант — идёт", "Мутант", [r"^mutant_walk"]),
    ("mutant_run", "Мутант — бежит", "Мутант", [r"^mutant_run"]),
    ("mutant_attack", "Мутант — атакует", "Мутант", [r"mutant_swipe", r"mutant_jump"]),
    ("mutant_death", "Мутант — умирает", "Мутант", [r"mutant_death"]),
]


def anims_of(src):
    info = os.path.join(ANIM, src.replace(".glb", "_info.json").replace("_anims_info", "_info"))
    if src == "anims_mixamo.glb":
        return sorted(json.load(open(os.path.join(ANIM, "anims_mixamo_info.json")))["actions"])
    return sorted(json.load(open(info))["animations"])


def main():
    names = {k: anims_of(v) for k, v in SOURCES.items()}
    out_path = os.path.join(ANIM, "anim_actions.json")
    old = {}
    if os.path.exists(out_path):
        old = {a["id"]: a.get("pinned") for a in json.load(open(out_path))["actions"]}
    actions, used = [], set()
    for aid, title, group, pats in ACTIONS:
        cands = []
        for src, lst in names.items():
            for n in lst:
                if any(re.search(p, n, re.I) for p in pats):
                    cands.append({"src": src, "anim": n})
                    used.add((src, n))
        actions.append({"id": aid, "name": title, "group": group, "candidates": cands, "pinned": old.get(aid)})
    data = {
        "_comment": ("Действия персонажей → анимации. candidates — подходящие по смыслу (смотреть на персонаже), "
                     "pinned — закреплённая ⭐ (игра проигрывает её для этого действия; null — ещё не выбрана). "
                     "Все анимации на скелете тел Tripo — подходят ко всем людям. Пересобрать: tools/anim_actions.py "
                     "(закреплённые сохраняются)."),
        "sources": {k: "export/anim/" + v for k, v in SOURCES.items()},
        "actions": actions,
        "unsorted": [{"src": s, "anim": n} for s, lst in names.items() for n in lst if (s, n) not in used],
    }
    json.dump(data, open(out_path, "w"), ensure_ascii=False, indent=1)
    empty = [a["id"] for a in actions if not a["candidates"]]
    print(f"→ {out_path}: действий {len(actions)}, без кандидатов: {empty}; анимаций вне действий: {len(data['unsorted'])}")


if __name__ == "__main__":
    main()
