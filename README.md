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

| Папка | id (для `drive_fetch.py --folder`) |
|---|---|
| 01 Стены — основы | `1iEYMW_n_5zYCVbtPREWMaCZrbAVWz28u` |
| 02 Стены — линии | `19kDUSj6B1q5Yg4bqbQXADsJ7fxwm1Mom` |
| 03 Стены — декор | `1DKiRF_miDQGDzqc2y-dXbtvOqrP2PeSj` |
| 04 Фасады | `1Obt5a88iOkl4IM68xALris9bdJbi4hM7` |
| 05 Мебель | `1MuuDaZ7sjM-a0Jr6IyePuCc7rXgMxflP` |
| 06 Верстаки | `10vQ2aJ7n9FLUNbe45XaUIZCugvzaM07Y` |
| 07 Контейнеры | `1NcYRXQWpMeJIg-Te60ZmyJI65OnpXOUL` |
| 08 Техника и машины | `1v1uE70JXuZ68tQl2eXsixJSotZ-jwAnV` |
| 09 Строительное и двери | `1PAst1du4N-nGD7gqAV1moz8T9fuyiwyk` |
| 10 Декор-объекты | `115YhMiHXbrjhTq-J7kTVvsHicp2vsNJm` |
| 11 Растения и точки ресурсов | `1NnKafHKCQ83qjtgBhqsgKIAUycdG9Yey` |
| 12 Предметы, инструменты, оружие, одежда | `1bJp7OilAS8mtEoGrc0bie5bJr6qN1F6t` |
| 13 Персонажи и существа | `1H_PLt4oX7a71q_IhjbdgYwnyu7gVmBeU` |
| 14 Прочее | `138NID0PQPlSHmOtKwMIgvfMm9X78PWhE` |

**Скачать раздел:** `python3 tools/drive_fetch.py --folder <id> tripo/` (с подпапками, имена как на Диске).

## Что сейчас

1. ⏳ **Все объекты** в стиле «кровать-образец» — `docs/TRIPO_OBJECTS.md`: 170 объектов, готовые запросы, папки на Диске.
   Автор делает по разделам, этот чат обрабатывает по мере появления, чат игры ставит в игру.
2. ☐ Стены и фасады из трёх слоёв — `docs/TRIPO_KIT.md` (запросы переписать под стиль образца).
3. ☐ Персонажи и существа — риг и анимации, отдельное задание.

## Файлы

```
CLAUDE.md                 — правила для чата моделей
docs/TRIPO.md             — как обрабатывать модели (главное)
docs/TRIPO_OBJECTS.md     — все объекты: стиль, готовые запросы, имена файлов, размеры, папки (главное для автора)
docs/TRIPO_KIT.md         — стены и фасады из трёх слоёв
docs/PLAN.md, plan.json   — все объекты из ОС, варианты, размеры, что готово
docs/TRIPO_REPORT.md      — отчёт обработки; docs/DEVIATIONS.md — отличия размеров от ОС
docs/FOR_GAME.md          — просьбы к игре; docs/LOG.md — журнал
tools/drive_fetch.py      — скачать с Диска; tools/tripo_process.py — обработка; tools/plan_status.py — чек-лист
tripo/                    — сюда скачиваются сырые модели (в git не попадают); rotate.json, color.json — настройки
export/                   — готовые модели для игры
renders/_review/          — листы превью (не коммитить большие — по одному на пачку)
```
