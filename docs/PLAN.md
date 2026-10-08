# План моделей (из ОС: tools/object-plan)

Источник — план объектов ОС (`object-constructor/tools/object-plan/js/0[3-5]-data-*.js`), выгрузка — `node tools/sync_plan.js <ОС>` → `docs/plan.json`, этот файл — `python3 tools/plan_status.py`.

Правила автора: **только idle**, каждый вариант — отдельно (`<id>_<вариант>_idle`); «сломанные/испорченные» и состояния (открыт, занят, пустой) — пропуск; размер — из ОС (если в плане другой — спросить автора); старые картинки ОС — не образец стиля (образец — `docs/ref/style/`).

Готово: **196 из 552** вариантов.

## Размер в плане ≠ ОС — **берём из плана** (решение автора 2026-10-08; в ОС поправить)

| id | План, см (берём) | ОС, см |
|---|---|---|
| `workbench_basic` | 160 × 95 | 230 × 137 |
| `workbench_electronics` | 140 × 95 | 230 × 182 |
| `recycler_bench` | 130 × 95 | 230 × 127 |
| `sewing_table` | 110 × 85 | 140 × 133 |
| `tool_saw` | 50 × 12 | 50 × 23 |
| `hatch_bunker` | 100 × 60 | 220 × 144 |
| `billboard_road` | 150 × 400 | 270 × 394 |

## `furniture`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `bed_single` | Кровать | 200 × 60 | ☑ Железная койка → `zheleznaya_koyka`<br>☑ Деревянная самодельная → `derevyannaya_samodelnaya`<br>☑ Низкая (матрас на подставке) → `nizkaya`<br>☑ Кровать с тумбой → `krovat_s_tumboy`<br>~~Испорченная / сломанная (для заброшенных комнат)~~ |  |
| `bunk_bed` | Двухъярусная койка | 200 × 180 | ☑ Металлическая → `metallicheskaya`<br>☑ Деревянная → `derevyannaya`<br>~~Трёхъярусная (позже)~~ |  |
| `table_wood` | Стол | 120 × 75 | ☑ Обеденный → `obedennyy`<br>☑ Письменный → `pismennyy`<br>☑ Складной → `skladnoy`<br>☑ Металлический (выдерживает больше) → `metallicheskiy`<br>☑ Кухонный стол → `kuhonnyy_stol` |  |
| `chair_wood` | Стул | 45 × 90 | ☑ Деревянный → `derevyannyy`<br>☑ Мягкий стул → `myagkiy_stul`<br>☑ Кресло → `kreslo`<br>☑ Табурет → `taburet`<br>☑ Барный стул → `barnyy_stul` |  |
| `toilet` | Унитаз | 40 × 75 | ☑ Фаянсовый со смывом → `fayansovyy_so_smyvom`<br>☑ Самодельный (ведро с сиденьем) → `samodelnyy`<br>☑ Сухой (компостный) → `suhoy`<br>~~Сломанный / заброшенный~~ |  |
| `sink_tap` | Раковина с краном | 80 × 90 | ☑ Кухонная → `kuhonnaya`<br>☑ Ванная → `vannaya`<br>☑ Умывальник → `umyvalnik`<br>☑ Уличная колонка → `ulichnaya_kolonka` |  |
| `bathtub` | Ванна | 170 × 60 | ☑ Чугунная → `chugunnaya`<br>☑ Пластиковая → `plastikovaya`<br>☑ Эмалированная → `emalirovannaya` |  |
| `cot_medical` | Медицинская койка | 190 × 80 | ☑ Складная → `skladnaya`<br>☑ Больничная → `bolnichnaya`<br>☑ Полевая → `polevaya` |  |
| `planter_box` | Грядка | 120 × 40 | ☐ Деревянный ящик → `derevyannyy_yaschik`<br>☐ Кирпичная грядка → `kirpichnaya_gryadka`<br>☐ Гидропонный лоток → `gidroponnyy_lotok`<br>~~Пустая (без грунта)~~ |  |
| `trade_stall` | Торговый прилавок | 160 × 110 | ☐ Прилавок → `prilavok`<br>☐ Тележка → `telezhka`<br>☐ Стол с товаром → `stol_s_tovarom` |  |

## `container`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `wardrobe` | Шкаф | 100 × 200 | ☑ Деревянный двустворчатый → `derevyannyy_dvustvorchatyy`<br>☑ Гардероб с зеркалом → `garderob_s_zerkalom`<br>☑ Металлический шкафчик → `metallicheskiy_shkafchik`<br>~~Открытый / выпотрошенный~~ |  |
| `shelf_wood` | Полка | 100 × 30 | ☑ Деревянная → `derevyannaya`<br>☑ Металлическая уголковая → `metallicheskaya_ugolkovaya`<br>☑ Угловая → `uglovaya`<br>☑ Двойная → `dvoynaya` |  |
| `barrel_water` | Бочка для воды | 60 × 90 | ☑ Пластиковая 200 л → `plastikovaya_200_l`<br>☑ Металлическая 200 л → `metallicheskaya_200_l`<br>☑ Деревянная 100 л → `derevyannaya_100_l`<br>☑ Малая канистра-бочонок 30 л → `malaya_kanistra_bochonok_30_l` |  |
| `tank_water` | Резервуар воды | 160 × 190 | ☑ Пластиковый 1000 л → `plastikovyy_1000_l`<br>☑ Бетонный 5000 л → `betonnyy_5000_l`<br>☑ Стальной цилиндр → `stalnoy_tsilindr`<br>☑ Подземный (люк) → `podzemnyy` |  |
| `battery_bank` | Аккумулятор | 60 × 40 | ☑ Автомобильный 12 В → `avtomobilnyy_12_v`<br>☑ Бункерная батарея (большая) → `bunkernaya_batareya`<br>~~Разряженный / вздувшийся~~ |  |
| `fuel_canister` | Канистра с топливом | 35 × 45 | ☑ 5 л → `5_l`<br>☑ 10 л → `10_l`<br>☑ 20 л (жерри) → `20_l`<br>~~Пустая~~ |  |
| `kitchen_counter` | Кухонная тумба | 120 × 90 | ☑ С раковиной → `s_rakovinoy`<br>☑ С ящиками → `s_yaschikami`<br>☑ Угловая → `uglovaya` |  |
| `first_aid_kit` | Аптечка | 25 × 18 | ☑ Домашняя → `domashnyaya`<br>☑ Автомобильная → `avtomobilnaya`<br>☑ Военная (богаче) → `voennaya`<br>~~Пустая~~ |  |
| `medicine_cabinet` | Аптечный шкафчик | 50 × 60 | ☑ Ванный → `vannyy`<br>☑ Медпункт (стеклянный) → `medpunkt`<br>☑ Металлический → `metallicheskiy` |  |
| `crate_wood` | Деревянный ящик | 60 × 50 | ☑ Малый → `malyy`<br>☑ Большой → `bolshoy`<br>☑ Военный → `voennyy`<br>~~Открытый / разграбленный~~<br>~~Разбитый~~ |  |
| `rack_metal` | Стеллаж металлический | 120 × 200 | ☐ С 3 полками → `s_3_polkami`<br>☐ С 5 полками → `s_5_polkami`<br>☐ Промышленный → `promyshlennyy` |  |
| `locker_metal` | Шкафчик металлический | 50 × 180 | ☐ Спортивный → `sportivnyy`<br>☑ Армейский → `armeyskiy`<br>☐ Офисный → `ofisnyy`<br>~~Взломанный~~ |  |
| `safe_metal` | Сейф | 50 × 60 | ☐ Настенный → `nastennyy`<br>☐ Напольный → `napolnyy`<br>☐ Сейф-ячейка → `seyf_yacheyka` |  |
| `toolbox` | Ящик с инструментами | 40 × 25 | ☐ Пластиковый → `plastikovyy`<br>☑ Металлический → `metallicheskiy`<br>☐ Полный набор → `polnyy_nabor` |  |
| `dumpster` | Мусорный бак | 130 × 110 | ☐ Зелёный → `zelenyy`<br>☐ Контейнер → `konteyner`<br>☐ Бочка → `bochka`<br>☐ Опрокинутый → `oprokinutyy` |  |
| `faction_stockpile` | Склад фракции | 200 × 120 | ☐ Ящики → `yaschiki`<br>☐ Палатка-склад → `palatka_sklad`<br>☐ Контейнер → `konteyner` |  |

## `machine`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `lamp_ceiling` | Лампа потолочная | 30 × 25 | ☑ Лампа накаливания → `lampa_nakalivaniya`<br>☑ Светодиодная → `svetodiodnaya`<br>☑ Аварийная (красная) → `avariynaya`<br>☑ Настольная → `nastolnaya`<br>☑ Подвесная с абажуром → `podvesnaya_s_abazhurom` |  |
| `radio_desk` | Радиоприёмник | 35 × 25 | ☑ Настольный → `nastolnyy`<br>☑ Ручной (с динамо) → `ruchnoy`<br>☑ Военная рация → `voennaya_ratsiya`<br>~~Сломанный~~ |  |
| `stove_heat` | Печь-буржуйка | 60 × 90 | ☑ Стальная бочка → `stalnaya_bochka`<br>☑ Кирпичная → `kirpichnaya`<br>☑ Походная → `pohodnaya` |  |
| `rain_collector` | Дождеуловитель | 110 × 60 | ☑ Плёнка и желоб → `plenka_i_zhelob`<br>☑ Крышная воронка → `kryshnaya_voronka`<br>☑ Большая площадка (для башни) → `bolshaya_ploschadka` |  |
| `water_pump` | Насос | 50 × 60 | ☑ Ручной рычажный → `ruchnoy_rychazhnyy`<br>☑ Электрический → `elektricheskiy`<br>☑ Бензиновый → `benzinovyy` |  |
| `water_purifier` | Очиститель воды | 60 × 100 | ☑ Керамический фильтр → `keramicheskiy_filtr`<br>☑ Кипячение на печи → `kipyachenie_na_pechi`<br>☑ Угольный фильтр → `ugolnyy_filtr`<br>☑ Химические таблетки (расходник) → `himicheskie_tabletki` |  |
| `solar_panel` | Солнечная панель | 120 × 80 | ☑ Малая 100 Вт → `malaya_100_vt`<br>☑ Большая 300 Вт → `bolshaya_300_vt`<br>☑ Складная портативная → `skladnaya_portativnaya`<br>~~Разбитая~~ |  |
| `wind_turbine` | Ветрогенератор | 100 × 300 | ☑ Малый горизонтальный → `malyy_gorizontalnyy`<br>☑ Вертикальный → `vertikalnyy`<br>☑ Самодельный из вентилятора → `samodelnyy_iz_ventilyatora` |  |
| `bike_generator` | Велогенератор | 120 × 110 | ☑ Стационарный → `statsionarnyy`<br>☑ Складной → `skladnoy` |  |
| `treadmill_generator` | Беговая дорожка-генератор | 160 × 120 | ☑ Беговая дорожка → `begovaya_dorozhka` |  |
| `fuel_generator` | Генератор на топливе | 70 × 60 | ☑ Портативный → `portativnyy`<br>☑ Стационарный → `statsionarnyy`<br>☑ Промышленный → `promyshlennyy` |  |
| `fridge` | Холодильник | 70 × 180 | ☑ Электрический → `elektricheskiy`<br>☑ Ящик со льдом → `yaschik_so_ldom`<br>☑ Морозильная камера → `morozilnaya_kamera` |  |
| `grow_lamp` | Лампа для урожая | 80 × 15 | ☑ Фиолетовая LED → `fioletovaya_led`<br>☑ Люминесцентная → `lyuminestsentnaya`<br>☑ Слабая → `slabaya` |  |
| `shelter_panel` | Панель убежища | 60 × 70 | ☑ Простой пульт → `prostoy_pult`<br>~~Экран с графиками (позже)~~ |  |
| `light_switch` | Выключатель | 8 × 12 | ☑ Клавишный → `klavishnyy`<br>☑ Рычажный (промышленный) → `rychazhnyy`<br>☑ Тумблер на щитке → `tumbler_na_schitke`<br>~~Сломанный~~ |  |
| `fuse_box` | Электрощит | 40 × 50 | ☑ Бытовой → `bytovoy`<br>☑ Промышленный → `promyshlennyy`<br>☑ Самодельный → `samodelnyy`<br>~~Сгоревший~~ |  |
| `stove_cook` | Плита | 70 × 90 | ☑ Газовая → `gazovaya`<br>☑ Электрическая → `elektricheskaya`<br>☑ Дровяная → `drovyanaya`<br>~~Сломанная~~ |  |
| `campfire` | Костёр | 80 × 50 | ☑ Простой → `prostoy`<br>☑ С камнями → `s_kamnyami`<br>☑ Костёр с котлом → `koster_s_kotlom`<br>☑ Догорающий → `dogorayuschiy` |  |
| `hydro_rack` | Гидропонная стойка | 100 × 180 | ☐ Малая → `malaya`<br>☐ Большая → `bolshaya` |  |
| `car_abandoned` | Брошенная машина | 450 × 160 | ☐ Седан → `sedan`<br>☐ Микроавтобус → `mikroavtobus`<br>☐ Грузовик → `gruzovik`<br>☐ Ржавая → `rzhavaya`<br>~~Перевёрнутая~~<br>~~Сгоревшая~~ |  |

## `item`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `lightbulb` | Лампочка | 6 × 12 | ☑ Накаливания → `nakalivaniya`<br>☑ Светодиодная (дольше) → `svetodiodnaya`<br>☑ Люминесцентная трубка → `lyuminestsentnaya_trubka`<br>~~Перегоревшая~~ |  |
| `water_tablets` | Таблетки для очистки воды | 6 × 10 | ☑ Хлорные → `hlornye`<br>☑ Йодные → `yodnye` |  |
| `bottle_water` | Бутылка с водой | 8 × 25 | ☑ Пластиковая 0,5 л → `plastikovaya_0_5_l`<br>☑ Пластиковая 1,5 л → `plastikovaya_1_5_l`<br>☑ Стеклянная → `steklyannaya`<br>☑ Фляга → `flyaga`<br>~~Пустая~~ |  |
| `power_cable` | Провод / кабель | 20 × 20 | ☑ Тонкий → `tonkiy`<br>☑ Силовой → `silovoy`<br>☑ Удлинитель → `udlinitel` |  |
| `battery_cell` | Батарейка | 3 × 6 | ☑ Одноразовая → `odnorazovaya`<br>☑ Перезаряжаемая → `perezaryazhaemaya`<br>~~Разряженная~~<br>~~Вздувшаяся (испорчена)~~ |  |
| `fuel_firewood` | Дрова | 40 × 15 | ☑ Поленья → `polenya`<br>☑ Вязанка хвороста → `vyazanka_hvorosta`<br>☑ Отсыревшие (горят хуже) → `otsyrevshie` |  |
| `food_canned` | Консервы | 8 × 10 | ☑ Тушёнка → `tushenka`<br>☑ Фасоль → `fasol`<br>☑ Рыбные → `rybnye`<br>☑ Сгущёнка → `sguschenka`<br>~~Вздувшаяся (опасная)~~ |  |
| `food_bread` | Хлеб / сухари | 20 × 10 | ☑ Хлеб → `hleb`<br>☑ Сухари (долго) → `suhari`<br>☑ Лепёшка → `lepeshka`<br>~~Заплесневевший~~ |  |
| `food_grain` | Зерно | 15 × 15 | ☑ Пшеница → `pshenitsa`<br>☑ Кукуруза → `kukuruza`<br>☑ Рис → `ris` |  |
| `meat_raw` | Сырое мясо | 15 × 8 | ☑ Кролик → `krolik`<br>☑ Собака (риск) → `sobaka`<br>☑ Птица → `ptitsa`<br>~~Тухлое~~ |  |
| `meat_cooked` | Приготовленное мясо | 15 × 8 | ☑ Жареное → `zharenoe`<br>☑ Варёное → `varenoe`<br>☑ Копчёное (долго хранится) → `kopchenoe` |  |
| `veg_potato` | Овощи (картофель, морковь) | 8 × 8 | ☑ Картофель → `kartofel`<br>☑ Морковь → `morkov`<br>☑ Помидор → `pomidor`<br>☑ Лук → `luk` |  |
| `meal_soup` | Готовое блюдо (суп, рагу) | 15 × 10 | ☑ Овощной суп → `ovoschnoy_sup`<br>☑ Мясное рагу → `myasnoe_ragu`<br>☑ Каша → `kasha` |  |
| `ration_dry` | Сухпаёк | 15 × 10 | ☑ Армейский → `armeyskiy`<br>☑ Спасательный набор → `spasatelnyy_nabor`<br>☑ Космический (редкий) → `kosmicheskiy` |  |
| `bandage` | Бинт | 10 × 6 | ☑ Стерильный → `sterilnyy`<br>☑ Самодельный из ткани → `samodelnyy_iz_tkani`<br>☑ Эластичный → `elastichnyy`<br>~~Использованный~~ |  |
| `antiseptic` | Антисептик | 6 × 14 | ☑ Спирт → `spirt`<br>☑ Перекись → `perekis`<br>☑ Йод → `yod` |  |
| `painkiller` | Обезболивающее | 6 × 8 | ☑ Таблетки → `tabletki`<br>☑ Ампула → `ampula`<br>☑ Сильное (редкое) → `silnoe` |  |
| `antibiotics` | Антибиотики | 6 × 8 | ☑ Широкого спектра → `shirokogo_spektra`<br>☑ Узкоспециальные → `uzkospetsialnye`<br>~~Просроченные (слабее)~~ |  |
| `splint` | Шина | 40 × 8 | ☑ Готовая → `gotovaya`<br>☑ Из досок и ткани → `iz_dosok_i_tkani` |  |
| `medical_kit` | Медицинский набор | 35 × 25 | ☑ Полевой → `polevoy`<br>☑ Хирургический → `hirurgicheskiy`<br>☑ Экстренный → `ekstrennyy` |  |
| `poison_vial` | Яд | 5 × 10 | ☑ Слабый → `slabyy`<br>☑ Сильный → `silnyy`<br>☑ Медленный → `medlennyy`<br>☑ Антидот (обратное) → `antidot` |  |
| `soap` | Мыло | 8 × 4 | ☑ Кусок мыла → `kusok_myla`<br>☑ Гель → `gel`<br>☑ Дезинфицирующее → `dezinfitsiruyuschee` |  |
| `seed_bag` | Семена | 10 × 14 | ☐ Картофель → `kartofel`<br>☐ Пшеница → `pshenitsa`<br>☐ Морковь → `morkov`<br>☐ Универсальная смесь → `universalnaya_smes` |  |
| `fertilizer_bag` | Удобрение | 25 × 35 | ☐ Компост → `kompost`<br>☐ Минеральное → `mineralnoe` |  |
| `mat_plank` | Доски | 100 × 10 | ☐ Доска → `doska`<br>☐ Брус → `brus`<br>☐ Фанера → `fanera`<br>☐ Обрезки → `obrezki` |  |
| `mat_log` | Брёвна | 120 × 20 | ☐ Полено → `poleno`<br>☐ Ствол → `stvol`<br>☐ Хворост → `hvorost` |  |
| `mat_scrap` | Металлолом | 25 × 15 | ☐ Лом → `lom`<br>☐ Обрезки → `obrezki`<br>☐ Ржавый → `rzhavyy` |  |
| `mat_sheet_metal` | Металлический лист | 100 × 3 | ☐ Тонкий → `tonkiy`<br>☐ Оцинкованный → `otsinkovannyy`<br>☐ Стальная плита → `stalnaya_plita` |  |
| `mat_pipe_metal` | Труба | 100 × 8 | ☐ Стальная → `stalnaya`<br>☐ ПВХ → `pvh`<br>☐ Медная → `mednaya` |  |
| `mat_nails` | Гвозди / крепёж | 6 × 4 | ☐ Гвозди → `gvozdi`<br>☐ Шурупы → `shurupy`<br>☐ Скобы → `skoby` |  |
| `mat_wire` | Проволока / провод | 20 × 20 | ☐ Медная → `mednaya`<br>☐ Стальная → `stalnaya`<br>☐ Колючая → `kolyuchaya` |  |
| `mat_cloth` | Ткань | 30 × 20 | ☐ Лоскут → `loskut`<br>☐ Полотно → `polotno`<br>☐ Брезент → `brezent` |  |
| `mat_rope` | Верёвка | 30 × 10 | ☐ Пенька → `penka`<br>☐ Нейлон → `neylon`<br>☐ Трос → `tros` |  |
| `mat_cement` | Цемент / стройматериалы | 30 × 40 | ☐ Мешок цемента → `meshok_tsementa`<br>☐ Смесь → `smes`<br>☐ Готовые блоки → `gotovye_bloki` |  |
| `part_mech` | Механические детали | 15 × 15 | ☐ Шестерни → `shesterni`<br>☐ Подшипники → `podshipniki`<br>☐ Пружины → `pruzhiny`<br>☐ Крепёж → `krepezh` |  |
| `part_electronic` | Электронные компоненты | 10 × 10 | ☐ Платы → `platy`<br>☐ Микросхемы → `mikroshemy`<br>☐ Конденсаторы → `kondensatory`<br>☐ Аккумуляторные элементы → `akkumulyatornye_elementy` |  |
| `part_rare_circuit` | Редкая схема | 10 × 10 | ☐ Военная плата → `voennaya_plata`<br>☐ Медицинский чип → `meditsinskiy_chip`<br>☐ Радиомодуль → `radiomodul` |  |
| `stone_chunk` | Кусок камня | 15 × 12 | ☐ Булыжник → `bulyzhnik`<br>☐ Щебень → `scheben`<br>☐ Гальки → `galki` |  |
| `soil_clump` | Грунт | 15 × 12 | ☐ Чернозём → `chernozem`<br>☐ Глина → `glina`<br>☐ Песок → `pesok` |  |
| `iron_ore` | Железная руда | 15 × 12 | ☐ Руда → `ruda`<br>☐ Обломки руды → `oblomki_rudy` |  |
| `coal_chunk` | Уголь | 15 × 12 | ☐ Каменный → `kamennyy`<br>☐ Древесный → `drevesnyy` |  |
| `mat_rubble` | Строительный мусор | 20 × 15 | ☐ Битый кирпич → `bityy_kirpich`<br>☐ Бетонная крошка → `betonnaya_kroshka` |  |
| `mat_glass` | Стекло | 30 × 30 | ☐ Лист стекла → `list_stekla`<br>☐ Осколки → `oskolki`<br>☐ Бутылочное стекло → `butylochnoe_steklo` |  |
| `repair_kit` | Ремонтный набор | 25 × 15 | ☐ Малый набор → `malyy_nabor`<br>☐ Набор механика → `nabor_mehanika`<br>☐ Электронный ремонтный набор → `elektronnyy_remontnyy_nabor` |  |
| `duct_tape` | Изолента / скотч | 10 × 10 | ☐ Изолента → `izolenta`<br>☐ Скотч → `skotch`<br>☐ Серебристая лента → `serebristaya_lenta` |  |
| `lock_padlock` | Навесной замок | 6 × 10 | ☐ Навесной → `navesnoy`<br>☐ Врезной → `vreznoy`<br>☐ Кодовый → `kodovyy`<br>~~Сломанный~~ |  |
| `key_generic` | Ключ | 3 × 8 | ☐ Обычный → `obychnyy`<br>☐ Ключ-карта → `klyuch_karta`<br>☐ Брелок с номером → `brelok_s_nomerom`<br>~~Сломанный~~ |  |
| `ammo_9mm` | Патроны 9 мм | 6 × 3 | ☐ Обычные → `obychnye`<br>☐ Бронебойные → `broneboynye`<br>☐ Самодельные → `samodelnye` |  |
| `ammo_shells` | Патроны для дробовика | 8 × 4 | ☐ Картечь → `kartech`<br>☐ Пуля → `pulya` |  |
| `note_diary` | Записка / дневник | 15 × 20 | ☐ Записка → `zapiska`<br>☐ Дневник → `dnevnik`<br>☐ Письмо → `pismo`<br>☐ Обрывок карты → `obryvok_karty` |  |
| `map_paper` | Карта | 30 × 20 | ☐ Карта района → `karta_rayona`<br>☐ Карта города → `karta_goroda`<br>☐ Схема убежища → `shema_ubezhischa` |  |

## `decor`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `clock_wall` | Часы настенные | 30 × 30 | ☑ Механические → `mehanicheskie`<br>☑ Электронные (нужна энергия) → `elektronnye`<br>~~Сломанные (остановились)~~ |  |
| `car_wreck` | Остов сгоревшей машины | 450 × 150 | ~~Сгоревшая~~<br>☐ Разобранная → `razobrannaya`<br>~~Перевёрнутая~~ |  |
| `street_lamp` | Уличный фонарь | 30 × 400 | ☐ Целый → `tselyy`<br>~~Разбитый~~<br>☐ Накренившийся → `nakrenivshiysya` |  |
| `billboard_road` | Рекламный щит | 150 × 400 | ☐ Целый → `tselyy`<br>☐ Проржавевший → `prorzhavevshiy`<br>☐ Заросший плющом → `zarosshiy_plyuschom` | размер из плана |
| `bench_street` | Скамейка | 150 × 80 | ☐ Деревянная → `derevyannaya`<br>☐ Каменная → `kamennaya`<br>~~Сломанная~~ |  |
| `grave_mound` | Могила | 150 × 60 | ☐ Холм → `holm`<br>☐ С крестом → `s_krestom`<br>☐ С табличкой → `s_tablichkoy`<br>☐ Общая → `obschaya` |  |
| `blood_stain` | Пятно крови | 100 × 20 | ☐ Лужа → `luzha`<br>☐ Брызги → `bryzgi`<br>☐ Следы → `sledy` |  |
| `faction_banner` | Знамя фракции | 60 × 200 | ☐ Знамя → `znamya`<br>☐ Граффити → `graffiti`<br>☐ Столб с символом → `stolb_s_simvolom` |  |
| `noticeboard` | Доска объявлений | 100 × 80 | ☐ Деревянная → `derevyannaya`<br>☐ Пробковая → `probkovaya` |  |

## `building`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `water_tower` | Водонапорная башня | 400 × 1000 | ☑ Кирпичная → `kirpichnaya`<br>☑ Стальная на опорах → `stalnaya_na_oporah`<br>~~Разрушенная~~ |  |
| `window_basic` | Окно | 100 × 100 | ☐ Целое → `tseloe`<br>~~Разбитое~~<br>☐ Заколоченное → `zakolochennoe`<br>☐ Решётка → `reshetka` |  |
| `stairs_wood` | Лестница | 110 × 260 | ☐ Деревянная → `derevyannaya`<br>☐ Металлическая → `metallicheskaya`<br>☐ Наклонная → `naklonnaya`<br>☐ Пожарная (наружная) → `pozharnaya` |  |
| `ladder_metal` | Металлическая лестница | 50 × 300 | ☐ Пристенная → `pristennaya`<br>☐ Стремянка → `stremyanka`<br>☐ Верёвочная → `verevochnaya` |  |
| `barricade_planks` | Баррикада | 110 × 200 | ☐ Доски на окне → `doski_na_okne`<br>☐ Мебель у двери → `mebel_u_dveri`<br>☐ Металлический заслон → `metallicheskiy_zaslon` |  |
| `fence_wire` | Забор с колючей проволокой | 200 × 150 | ☐ Сетка → `setka`<br>☐ Колючая проволока → `kolyuchaya_provoloka`<br>☐ Деревянный частокол → `derevyannyy_chastokol` |  |
| `tent_camp` | Палатка | 220 × 140 | ☐ Одноместная → `odnomestnaya`<br>☐ Большая → `bolshaya`<br>☐ Полевая брезентовая → `polevaya_brezentovaya` |  |
| `watchtower` | Наблюдательная вышка | 200 × 500 | ☐ Деревянная → `derevyannaya`<br>☐ Металлическая → `metallicheskaya` |  |

## `resource`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `well_hand` | Колодец / скважина | 90 × 130 | ☑ Ручной колодец с воротом → `ruchnoy_kolodets_s_vorotom`<br>☑ Скважина с ручной помпой → `skvazhina_s_ruchnoy_pompoy`<br>☑ Скважина с электронасосом → `skvazhina_s_elektronasosom`<br>~~Пересохший~~ |  |
| `scrap_pile` | Куча хлама | 120 × 80 | ☐ Металлолом → `metallolom`<br>☐ Строительный хлам → `stroitelnyy_hlam`<br>☐ Электроника → `elektronika`<br>☐ Бытовой хлам → `bytovoy_hlam` |  |

## `tool`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `bucket` | Ведро | 30 × 30 | ☑ Металлическое → `metallicheskoe`<br>☑ Пластиковое → `plastikovoe`<br>~~Дырявое (сломано)~~ |  |
| `cooking_pot` | Кастрюля / котелок | 25 × 20 | ☑ Алюминиевая → `alyuminievaya`<br>☑ Котелок → `kotelok`<br>☑ Чугунный → `chugunnyy` |  |
| `tool_can_opener` | Консервный нож | 15 × 8 | ☑ Ручной → `ruchnoy`<br>☑ Ключ-открывашка → `klyuch_otkryvashka` |  |
| `tool_hammer` | Молоток | 30 × 10 | ☐ Столярный → `stolyarnyy`<br>☐ Кувалдочка → `kuvaldochka`<br>☐ Ржавый (слабее) → `rzhavyy` |  |
| `tool_wrench` | Гаечный ключ | 30 × 8 | ☐ Разводной → `razvodnoy`<br>☐ Рожковый → `rozhkovyy`<br>☐ Набор ключей → `nabor_klyuchey` |  |
| `tool_screwdriver` | Отвёртка | 20 × 4 | ☐ Крестовая → `krestovaya`<br>☐ Плоская → `ploskaya`<br>☐ Набор → `nabor` |  |
| `tool_saw` | Пила | 50 × 12 | ☐ Ножовка → `nozhovka`<br>☐ Двуручная → `dvuruchnaya`<br>☐ Бензопила (редкая, шумная) → `benzopila` | размер из плана |
| `tool_axe` | Топор | 35 × 60 | ☐ Колун → `kolun`<br>☐ Пожарный → `pozharnyy`<br>☐ Каменный самодельный → `kamennyy_samodelnyy` |  |
| `tool_pickaxe` | Кирка | 35 × 60 | ☐ Стальная → `stalnaya`<br>☐ Самодельная → `samodelnaya`<br>☐ Отбойный молоток (энергия) → `otboynyy_molotok` |  |
| `tool_shovel` | Лопата | 30 × 110 | ☐ Штыковая → `shtykovaya`<br>☐ Совковая → `sovkovaya`<br>☐ Сапёрная (складная) → `sapernaya` |  |
| `tool_sledge` | Кувалда | 30 × 90 | ☐ Малая → `malaya`<br>☐ Большая → `bolshaya`<br>☐ Молот-кирка → `molot_kirka` |  |
| `tool_crowbar` | Лом | 70 × 8 | ☐ Стальной → `stalnoy`<br>☐ Гвоздодёр → `gvozdoder`<br>☐ Монтировка → `montirovka` |  |
| `tool_lockpick` | Отмычки | 10 × 5 | ☐ Набор → `nabor`<br>☐ Самодельные → `samodelnye` |  |
| `tool_flashlight` | Фонарик | 10 × 25 | ☐ Ручной → `ruchnoy`<br>☐ Налобный → `nalobnyy`<br>☐ С динамо (без батареек) → `s_dinamo` |  |
| `tool_soldering` | Паяльник | 25 × 5 | ☐ Сетевой → `setevoy`<br>☐ Газовый → `gazovyy` |  |
| `tool_knife` | Нож | 25 × 5 | ☐ Кухонный → `kuhonnyy`<br>☐ Охотничий → `ohotnichiy`<br>☐ Складной → `skladnoy`<br>☐ Ржавый → `rzhavyy` |  |

## `clothing`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `backpack` | Рюкзак | 35 × 45 | ☐ Школьный (малый) → `shkolnyy`<br>☐ Туристический → `turisticheskiy`<br>☐ Военный (большой) → `voennyy`<br>☐ Сумка через плечо → `sumka_cherez_plecho` |  |
| `cloth_jacket` | Куртка | 50 × 70 | ☐ Кожаная → `kozhanaya`<br>☐ Ветровка → `vetrovka`<br>☐ Худи → `hudi`<br>☐ Рабочая роба → `rabochaya_roba` |  |
| `cloth_pants` | Штаны | 40 × 80 | ☐ Джинсы → `dzhinsy`<br>☐ Камуфляж → `kamuflyazh`<br>☐ Спортивные → `sportivnye` |  |
| `cloth_boots` | Ботинки | 30 × 20 | ☐ Кроссовки → `krossovki`<br>☐ Берцы → `bertsy`<br>☐ Резиновые сапоги → `rezinovye_sapogi` |  |
| `cloth_gloves` | Перчатки | 20 × 15 | ☐ Рабочие → `rabochie`<br>☐ Кожаные → `kozhanye`<br>☐ Тактические → `takticheskie` |  |
| `mask_gas` | Противогаз | 25 × 30 | ☐ Военный → `voennyy`<br>☐ Респиратор → `respirator`<br>☐ Самодельный → `samodelnyy` |  |
| `vest_armor` | Бронежилет | 45 × 60 | ☐ Самодельный → `samodelnyy`<br>☐ Полицейский → `politseyskiy`<br>☐ Военный → `voennyy` |  |

## `workbench`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `workbench_basic` | Верстак | 160 × 95 | ☐ Деревянный базовый → `derevyannyy_bazovyy`<br>☐ Металлический (тяжёлый) → `metallicheskiy`<br>☐ Складной походный → `skladnoy_pohodnyy`<br>☐ Верстак с тисками → `verstak_s_tiskami`<br>~~Сломанный~~ | размер из плана |
| `workbench_electronics` | Электронный верстак | 140 × 95 | ☐ Настольный → `nastolnyy`<br>☐ Мобильная стойка → `mobilnaya_stoyka` | размер из плана |
| `recycler_bench` | Стол разборки | 130 × 95 | ☐ Ручной → `ruchnoy`<br>☐ С тисками и лом → `s_tiskami_i_lom` | размер из плана |
| `sewing_table` | Швейный стол | 110 × 85 | ☐ Ручная машина → `ruchnaya_mashina`<br>☐ Педальная → `pedalnaya` | размер из плана |

## `plant`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `plant_potato` | Картофель (растение) | 40 × 40 | ☐ Картофель → `kartofel`<br>☐ Морковь → `morkov`<br>☐ Помидор → `pomidor`<br>☐ Кукуруза → `kukuruza` |  |
| `plant_wheat` | Пшеница (растение) | 50 × 80 | ☐ Пшеница → `pshenitsa`<br>☐ Рожь → `rozh`<br>☐ Ячмень → `yachmen` |  |
| `plant_tree` | Дерево | 160 × 450 | ☐ Сосна → `sosna`<br>☐ Дуб → `dub`<br>☐ Сухое дерево → `suhoe_derevo`<br>☐ Пень → `pen`<br>☐ Молодое → `molodoe` |  |
| `bush_berry` | Ягодный куст | 80 × 70 | ☐ Малина → `malina`<br>☐ Черника → `chernika`<br>☐ Ядовитые ягоды → `yadovitye_yagody`<br>☐ Снотворные ягоды → `snotvornye_yagody` |  |

## `block`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `block_dirt` | Земля | 100 × 100 | ☐ Сухая земля → `suhaya_zemlya`<br>☐ Земля с травой (верх) → `zemlya_s_travoy`<br>☐ Глина → `glina`<br>☐ Песок → `pesok`<br>☐ Мокрая земля → `mokraya_zemlya` |  |
| `block_stone` | Камень | 100 × 100 | ☐ Гранит → `granit`<br>☐ Известняк → `izvestnyak`<br>☐ Слоистый → `sloistyy` |  |
| `block_concrete` | Бетон | 100 × 100 | ☐ Бетон → `beton`<br>☐ Железобетон (арматура) → `zhelezobeton`<br>☐ Бетонная плита → `betonnaya_plita` |  |
| `block_brick` | Кирпич | 100 × 100 | ☐ Красный кирпич → `krasnyy_kirpich`<br>☐ Штукатурка → `shtukaturka`<br>☐ Облицованный → `oblitsovannyy` |  |
| `block_wood` | Деревянная стена / пол | 100 × 100 | ☐ Доски → `doski`<br>☐ Фанера → `fanera`<br>☐ Паркет → `parket`<br>☐ Обшивка → `obshivka` |  |
| `block_metal` | Металлическая плита | 100 × 100 | ☐ Лист → `list`<br>☐ Решётка → `reshetka`<br>☐ Ребристая → `rebristaya` |  |
| `block_asphalt` | Асфальт | 100 × 100 | ☐ Асфальт → `asfalt`<br>☐ Трещины → `treschiny`<br>☐ Тротуар → `trotuar` |  |
| `block_rubble` | Завал | 100 × 100 | ☐ Кирпичный завал → `kirpichnyy_zaval`<br>☐ Бетонный → `betonnyy`<br>☐ Смешанный → `smeshannyy` |  |
| `block_ore_iron` | Железная руда (пласт) | 100 × 100 | ☐ Богатая жила → `bogataya_zhila`<br>☐ Бедная → `bednaya` |  |
| `block_coal` | Угольный пласт | 100 × 100 | ☐ Пласт → `plast`<br>☐ Вкрапления → `vkrapleniya` |  |
| `block_bedrock` | Неразрушаемая порода | 100 × 100 | ☐ Тёмная порода → `temnaya_poroda`<br>☐ Слоистая (видны пласты) → `sloistaya`<br>☐ Фундамент бункера → `fundament_bunkera` |  |

## `door`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `door_wood` | Дверь деревянная | 100 × 200 | ☐ Внутренняя → `vnutrennyaya`<br>☐ Входная → `vhodnaya`<br>☐ Дверь со стеклом → `dver_so_steklom`<br>☐ Выбитая → `vybitaya`<br>☐ Запертая → `zapertaya` |  |
| `door_metal` | Дверь металлическая | 100 × 200 | ☐ Стальная → `stalnaya`<br>☐ Бронированная → `bronirovannaya`<br>☐ Противопожарная → `protivopozharnaya` |  |
| `hatch_bunker` | Люк бункера | 100 × 60 | ☐ Люк с колесом → `lyuk_s_kolesom`<br>☐ Ляда → `lyada`<br>☐ Шлюз (двойной) → `shlyuz` | размер из плана |
| `signpost_fork` | Указатель развилки | 80 × 220 | ☐ Дорожный знак → `dorozhnyy_znak`<br>☐ Самодельный указатель → `samodelnyy_ukazatel`<br>☐ Ржавый (частично читается) → `rzhavyy`<br>☐ Билборд → `bilbord` |  |

## `weapon`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `weapon_bat` | Бейсбольная бита | 90 × 10 | ☐ Деревянная → `derevyannaya`<br>☐ Алюминиевая → `alyuminievaya`<br>☐ С гвоздями → `s_gvozdyami` |  |
| `weapon_pipe` | Труба-дубинка | 80 × 8 | ☐ Стальная труба → `stalnaya_truba`<br>☐ С обмоткой → `s_obmotkoy`<br>☐ С шипами → `s_shipami` |  |
| `weapon_machete` | Мачете | 70 × 8 | ☐ Мачете → `machete`<br>☐ Топор-мачете → `topor_machete`<br>☐ Нож-кукри → `nozh_kukri` |  |
| `weapon_pistol` | Пистолет | 20 × 14 | ☐ 9 мм → `9_mm`<br>☐ Револьвер → `revolver`<br>☐ Самодельный → `samodelnyy` |  |
| `weapon_shotgun` | Дробовик | 100 × 15 | ☐ Помповый → `pompovyy`<br>☐ Двустволка → `dvustvolka`<br>☐ Обрез → `obrez` |  |
| `weapon_bow` | Лук | 70 × 110 | ☐ Охотничий → `ohotnichiy`<br>☐ Самодельный → `samodelnyy`<br>☐ Блочный → `blochnyy` |  |
| `trap_bear` | Капкан / ловушка | 40 × 10 | ☐ Капкан → `kapkan`<br>☐ Петля → `petlya`<br>☐ Яма с кольями → `yama_s_kolyami` |  |

## `character`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `survivor_base` | Выживший (шаблон) | 100 × 180 | ☐ Игрок → `igrok`<br>☐ Член группы → `chlen_gruppy`<br>☐ Независимый NPC → `nezavisimyy_npc`<br>☐ Раненый → `ranenyy`<br>☐ Заражённый → `zarazhennyy` |  |
| `raider_human` | Рейдер / бандит | 100 × 180 | ☐ Мародёр → `maroder`<br>☐ Бандит с оружием → `bandit_s_oruzhiem`<br>☐ Разведчик → `razvedchik`<br>☐ Лидер банды → `lider_bandy` |  |
| `trader_npc` | Торговец | 100 × 180 | ☐ Бродячий → `brodyachiy`<br>☐ Лавочник → `lavochnik`<br>☐ Меняла → `menyala` |  |

## `creature`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `zombie_walker` | Зомби (ходячий) | 100 × 180 | ☐ Ходячий → `hodyachiy`<br>☐ Раненый (ползёт) → `ranenyy`<br>☐ Одетый (лут) → `odetyy`<br>☐ Мёртвая толпа (группа) → `mertvaya_tolpa` |  |
| `zombie_runner` | Зомби (быстрый) | 100 × 180 | ☐ Бегун → `begun`<br>☐ Прыгун → `prygun` |  |
| `zombie_brute` | Зомби (тяжёлый) | 120 × 200 | ☐ Здоровяк → `zdorovyak`<br>☐ Броневой → `bronevoy` |  |
| `dog_feral` | Дикая собака | 90 × 60 | ☐ Одиночная → `odinochnaya`<br>☐ Стая → `staya`<br>☐ Больная → `bolnaya` |  |
| `rabbit_wild` | Кролик | 35 × 25 | ☐ Кролик → `krolik`<br>☐ Заяц → `zayats`<br>☐ Птица → `ptitsa` |  |
| `rat_pest` | Крыса | 25 × 10 | ☐ Крыса → `krysa`<br>☐ Стая → `staya` |  |
| `mutant_crawler` | Мутант-ползун | 140 × 60 | ☐ Ползун → `polzun`<br>☐ Плевальщик → `plevalschik` |  |

## `corpse`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `corpse_human` | Останки человека | 180 × 30 | ☐ Свежее → `svezhee`<br>☐ Разложившееся → `razlozhivsheesya`<br>☐ Скелет → `skelet`<br>☐ Сожжённое → `sozhzhennoe`<br>☐ Заражённое → `zarazhennoe` |  |
| `corpse_zombie` | Останки зомби | 180 × 30 | ☐ Свежее → `svezhee`<br>~~Гнилое~~ |  |

## `special`

| id | Название | Размер (ОС), см | Варианты → файл | |
|---|---|---|---|---|
| `pyre_pile` | Погребальный костёр | 150 × 80 | ☐ Костёр → `koster`<br>☐ Печь для сжигания → `pech_dlya_szhiganiya` |  |
