# Модели для игры «Shelter»

3D-модели для игры про выживание в бункере — **[mrbobsterx-boop/godot](https://github.com/mrbobsterx-boop/godot)**
(Godot 4.7, мир в настоящем 3D, как Fallout Shelter: бункер в разрезе, вид сбоку). Данные объектов (что есть, размеры,
варианты) — **Object Constructor (ОС)**: [mrbobsterx-boop/object-constructor](https://github.com/mrbobsterx-boop/object-constructor).

## Порядок работы

```
Tripo (автор) ──► Google Диск «Shelter Tripo» (сырые GLB, по папкам)
              ──► этот репозиторий: tools/drive_fetch.py → tripo/ → tools/tripo_process.py → export/<имя>_idle.glb
              ──► игра: assets/models/ (чат игры)
```

| Кто | Что делает |
|---|---|
| **Автор** | Делает модели в Tripo по готовым запросам, кладёт GLB в нужную папку на Google Диске |
| **Чат моделей (этот)** | Скачивает с Диска, обрабатывает (поворот, размер, облегчение, текстуры), лист превью, `export/` |
| **Чат игры** | Забирает `export/` в игру, проверяет в игре, присылает автору снимки |

## Google Диск

Папка **«Shelter Tripo»** (доступ по ссылке — чтение): https://drive.google.com/drive/folders/1WS4lqCjsxTzgIn6uyvNmC9SVGttSojOb
- `00 Проба стиля (одна комната)` → `A — Low poly`, `B — Реализм (как сейчас)`, `C — Рисованный (как Fallout Shelter)`
- `01 Стены — основы`, `02 Стены — линии`, `03 Стены — декор`, `04 Фасады`, `05 Мебель`, `06 Верстаки`,
  `07 Контейнеры`, `08 Техника и машины`, `09 Строительное и двери`, `10 Декор-объекты`,
  `11 Растения и точки ресурсов`, `12 Предметы…`, `13 Персонажи и существа`, `14 Прочее`

**Скачать:**
- проба стиля: `python3 tools/drive_fetch.py --style-test` → `tripo/style_test/a|b|c/<имя>.glb`;
- любая папка: `python3 tools/drive_fetch.py --folder <id папки> tripo/<куда>` (id — из ссылки на папку);
- по списку `tripo/drive.json` (имя → id файла): `python3 tools/drive_fetch.py`.

## Что сейчас

1. ⏳ **Проба стиля** — `docs/TRIPO_STYLE_TEST.md`: 18 предметов комнаты × 3 стиля (оболочку — пол, стены, потолок —
   строит игра). Обработка → `export/style_test/a|b|c/<имя>_idle.glb`. Автор сравнит в игре (Tab — стиль).
2. ☐ Автор выбирает стиль → общий план всех объектов в этом стиле (`docs/TRIPO_OBJECTS.md`), пачки по разделам.
3. ☐ Стены и фасады из трёх слоёв (основа, линии, декор) — `docs/TRIPO_KIT.md` (запросы — переписать под стиль).

Уже в игре: 9 верстаков (`export/workbench_*`, `recycler_bench_*`, `sewing_table_*`) — стиль B, с картинок ОС.

## Файлы

```
CLAUDE.md                 — правила для чата моделей
docs/TRIPO.md             — как обрабатывать модели (главное)
docs/TRIPO_STYLE_TEST.md  — проба стиля: предметы, размеры, готовые запросы
docs/TRIPO_KIT.md         — стены и фасады из трёх слоёв
docs/PLAN.md, plan.json   — все объекты из ОС, варианты, размеры, что готово
docs/TRIPO_REPORT.md      — отчёт обработки; docs/DEVIATIONS.md — отличия размеров от ОС
docs/FOR_GAME.md          — просьбы к игре; docs/LOG.md — журнал
tools/drive_fetch.py      — скачать с Диска; tools/tripo_process.py — обработка; tools/plan_status.py — чек-лист
tripo/                    — сюда скачиваются сырые модели (в git не попадают); rotate.json, color.json — настройки
export/                   — готовые модели для игры
renders/_review/          — листы превью
```
