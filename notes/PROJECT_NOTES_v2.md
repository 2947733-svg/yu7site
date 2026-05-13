# yu7.site — состояние проекта на 2026-05-06

> **Файл для следующего чата Claude.** Содержит полный контекст проекта, историю действий, текущее состояние и список открытых задач.

---

## 🎯 Главное правило

### НЕ ВРИ И НЕ ПРИДУМЫВАЙ

Каждый факт перед публикацией проверять. Если не знаешь — спрашивай или предложи источник из «Источники материалов». Лучше пустота, чем выдумка.

При ревью старого контента — если найдёшь придуманное предыдущей версией Claude, **сразу скажи Roman'у конкретно, покажи текст**.

---

## 👤 Кто такой Roman

- **Имя:** Roman / Herbert Wells (@HerbertWells, @Herbert_Wells)
- **Авто:** Xiaomi YU7 Max
- **Стиль общения:** короткий, прямой, без филлеров. Не любит «давайте разберёмся».
- **Команды терминала** — сразу целиком, с полными путями, без пошаговых подтверждений.
- **Правки HTML** — минимально-инвазивные, классы `article.css` сохранять.

---

## 🏗️ Что такое yu7.site

Независимый русскоязычный справочник по Xiaomi YU7 для владельцев и покупателей. Статический сайт (HTML/CSS), общий `article.css`. **40+ страниц.**

- **Хостинг:** Beget, путь `/var/www/u9408526/data/www/yu7.site/`
- **Деплой:** WinSCP (`u9408526@31.31.196.158`)
- **Авторская позиция:** независимый справочник, **не аффилирован с Xiaomi**
- **Источник фактов:** сообщество @XiaomiEVclub и другие (см. блок «Источники» на главной)

---

## 🚫 Off-limits темы (НЕ публикуем)

| Код | Тема | Почему |
|---|---|---|
| C4 | Модифицированный Yandex Maps APK | Нарушение лицензии |
| C6 | Локация T-box в YU7 | Безопасность владельцев |
| C10 | HyperOS notification settings | Слишком частые изменения |
| C11 | Bypass `a.gray.generic` APK install error | Серая зона |

---

## 📺 YouTube канал

- **Канал:** «V M», ID `UC17b41rfOu7ff5oK2cgtWSg`
- **Handle:** `@ВладимирПерепечёный-е9х` (автоген, желательно поменять)
- **Назначение:** хостинг видео-инструкций со ссылками с yu7.site
- **TODO:** переименовать канал в «YU7.site» или подобное, поменять handle

### CSS-классы для встраивания (УЖЕ ЕСТЬ в article.css — не дублировать!)

```html
<!-- Эталонный шаблон из существующего no-power.html -->
<div class="video-embed">
    <div class="video-embed-header">
        <span class="yt">YouTube</span>
        <span>Заголовок видео</span>
    </div>
    <div class="video-embed-frame">
        <iframe src="https://www.youtube.com/embed/{ID}" 
                title="..." 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                allowfullscreen 
                loading="lazy"></iframe>
    </div>
</div>
```

`.video-embed-frame` по умолчанию **9:16** (вертикальные Shorts). Для горизонтальных 16:9 видео добавлять inline `style="aspect-ratio: 16 / 9; max-width: 100%;"`.

Для предупреждений использовать существующие `.note .note-warning`, `.note .note-danger`, `.note .note-info`:

```html
<div class="note note-danger">
    <span class="note-icon">🚫</span>
    <div><b>Опасно.</b> Текст предупреждения.</div>
</div>
```

---

## 📺 Каталог наших видео на канале V M

### ✅ Заполнены метаданные + встроены на сайт

| ID YouTube | Тема | Просмотры | Где на сайте |
|---|---|---|---|
| `4SitJE9ubQM` | Карбон 1/5 | 3 | repair.html ✅ |
| `NunAYM_-YB4` | Карбон 2/5 | 2 | repair.html ✅ |
| `idLaOpEUer4` | Карбон 3/5 | 4 | repair.html ✅ |
| `EHKzyaAOPSg` | Карбон 4/5 ⭐ | **14 302** | repair.html ✅ |
| `mzoQOlWqgf8` | Карбон 5/5 ⭐ | **21 039** | repair.html ✅ |
| `0yeyZ6LpEow` | Перенос внутренностей руля YU7 ⭐ | **1 274** | repair.html ✅ (с warning SRS) |
| `DzTEk-d5pqY` | Разборка подушки руля YU7 — ознакомительно | новое | repair.html ✅ (с danger SRS) |
| `kLi85f0uNJQ` | Снятие блока XiaoAi (для SU7) | 0 | repair.html ✅ (с info — для SU7) |
| `vM6gxuXoVD0` | Замена фильтра YU7 | 8 | maintenance.html ✅ |
| `cICTBnI48fI` | Замена фильтра SU7 | 1 | maintenance.html ✅ (с info — для SU7) |
| `4e6Q7B5AWh0` | CDC — адаптивная подвеска | 1 | wheels-specs.html ✅ |
| `hK00SD8VsTg` | BT-ключ on approach | 1 | keys.html ✅ |
| `OUb92u48GGY` | Замена батарейки CR2450 в ключе | 974 | battery-key.html (давно встроено) |
| `ZQYH8mwlYhU` | Подача питания через лючок | 925 | no-power.html (давно встроено) |
| `zFgJ9wKG6vE` | V2L | 10 | v2l.html (давно встроено) |

**Итого: 15 видео полностью обработаны.**

### ⚠️ Возможные дубли среди обычных видео — РАЗОБРАТЬСЯ В СЛЕДУЮЩЕМ ЧАТЕ

| Что есть | Возможный дубль | Действие |
|---|---|---|
| `reply 779 video` (1:24, 1 просм) | `8ufNnDRXsQM` (1:24, 0 просм, заполнено) | Если у `reply 779` больше просмотров — переключить ID в HTML, удалить новый-дубль |
| `reply 366 video` (4:31, 2 просм) | `4e6Q7B5AWh0` (4:31, 0 просм, **уже встроен на wheels-specs.html**) | Если у `reply 366` больше просмотров — переключить ID на сайте, удалить новый-дубль |
| `SU7 xiaoai block removal` (Черновик, 6:29) | `kLi85f0uNJQ` (опубликован, 6:29) | Удалить Черновик — точный дубль |

### Что точно нужно сделать в новом чате:
1. Открыть `studio.youtube.com/video/{reply 779 ID}/edit` — сравнить с `8ufNnDRXsQM`
2. Открыть `studio.youtube.com/video/{reply 366 ID}/edit` — сравнить с `4e6Q7B5AWh0`
3. Удалить черновик `SU7 xiaoai block removal`
4. **Если переключаем ID** — обновить `repair.html` (подлокотник) и `wheels-specs.html` (CDC)

---

## 🗑️ Удалено в предыдущей сессии

6 новых-дублей карбона/BT-ключа от 5 мая 2026:
- ✅ `8FjQBQEHTGE` — BT-ключ
- ✅ `DFZ8UwSyhkU` — Карбон 1/5
- ✅ `2-DF234US3A` — Карбон 2/5
- ✅ `oWpRFQvXfwo` — Карбон 3/5
- ✅ `iRdG_HxsWSQ` — Карбон 4/5
- ✅ `ALRhGSTwZFA` — Карбон 5/5

**Все старые reply-видео с просмотрами остались целыми и невредимыми.**

---

## 🛠️ Координаты Chrome MCP для удаления YouTube-видео (проверены)

```
1. Открыть studio.youtube.com/video/{ID}/edit
2. 3-точки в правом верхнем углу: (1268, 94)
3. "Удалить" в меню: (1338, 169)
4. Галочка подтверждения: (546, 429)
5. "Удалить навсегда": (962, 514)
6. Verify: youtube.com/shorts/{ID} → "Видео недоступно"
```

**Важные принципы для Chrome MCP:**
- Прямой URL `studio.youtube.com/video/{ID}/edit` всегда быстрее списка Shorts
- Для просмотра публичного состояния: `youtube.com/shorts/{ID}` или `youtube.com/watch?v={ID}`
- НЕ кликать по списку и не скроллить — координаты после скролла нестабильны
- Перед редактированием **всегда** проверять имя файла в превью (`reply_NNN_video.mp4` для старых, кастомные для новых)
- Кнопка «Отменить изменения» = `(1063, 94)` — спасает если ошибся ДО сохранения

---

## 📁 Применённый патч сайта (готов к деплою!)

### Что в патче `yu7site_videos_patch.zip`:

| Файл | Изменение |
|---|---|
| `repair.html` | +Раздел «Видео-инструкции» (карбон 1-5, перенос руля, подушка SRS, XiaoAi для SU7) — **8 видео** |
| `maintenance.html` | +Раздел «Видео-инструкции: салонный фильтр» — **2 видео** |
| `wheels-specs.html` | +Блок «Видео: что такое CDC» — **1 видео** |
| `keys.html` | +Видео «Режим On approach» в разделе «Смартфон как ключ» — **1 видео** |
| `search-index.json` | Перегенерированы text-поля для 4 обновлённых страниц |
| `article.css` | **НЕ ИЗМЕНЁН** — все классы уже были |

### Команды для деплоя (Roman должен выполнить):

```powershell
# 1. Бэкап
$ts = Get-Date -Format 'yyyy-MM-dd_HHmm'
Copy-Item -Path "C:\claude-test\yu7-digest\site_live" -Destination "C:\Claude\BackUp\site_live_before_videos_$ts" -Recurse

# 2. Распаковать ZIP в site_live (с заменой)
Expand-Archive -Path "C:\Claude\yu7site_videos_patch.zip" -DestinationPath "C:\claude-test\yu7-digest\site_live" -Force

# 3. Локальная проверка
cd C:\claude-test\yu7-digest\site_live
npx serve .
# Открыть http://localhost:3000/repair.html — должны быть 8 видео
# Открыть http://localhost:3000/maintenance.html — 2 видео
# Открыть http://localhost:3000/wheels-specs.html — 1 видео CDC
# Открыть http://localhost:3000/keys.html — 1 видео BT-ключа

# 4. Загрузка через WinSCP на хостинг u9408526@31.31.196.158
#    Загрузить 5 файлов в /var/www/u9408526/data/www/yu7.site/:
#    repair.html, maintenance.html, wheels-specs.html, keys.html, search-index.json
```

### Проверка после деплоя:
- https://yu7.site/repair.html — раздел «Видео-инструкции» с 8 видео
- https://yu7.site/maintenance.html — фильтры YU7 + SU7
- https://yu7.site/wheels-specs.html — CDC видео
- https://yu7.site/keys.html — BT-ключ on approach
- Поиск по сайту: «карбон», «фильтр», «CDC», «on approach» — должны находиться

---

## 📂 Структура файлов и папок Roman'а

### Локальная машина (Windows):
- `C:\claude-test\yu7-digest\` — корень проекта
- `C:\claude-test\yu7-digest\site_live\` — рабочая копия сайта (для деплоя)
- `C:\claude-test\yu7-digest\collector\` — Telethon-скрипты:
  - `collect_private.py` (с backfill `--since/--until`)
  - `fetch_threads.py`
  - `build_catalog_from_data.py`
  - `retry_skipped.py` (не запущен!)
  - `session_yu7.session` (45 КБ, КРИТИЧНО)
  - `.env` (TG_API_ID, TG_API_HASH, TG_PHONE)
- `C:\claude-test\yu7-digest\data\` — JSON-сборы
- `C:\claude-test\yu7-digest\data\threads\YYYY-MM-DD\` — снапшоты тредов
- `C:\claude-test\yu7-digest\_youtube_upload\` — переименованные видео для заливки
- `C:\Claude\BackUp\` — бэкапы сайта

### Telegram-источники:
| Канал | Назначение |
|---|---|
| @XiaomiEVclub | Главный (FAQ-тред 5358) |
| @XiaomiY7MAX | Видео-инструкции (FAQ-тред 9) |
| @Xiaomi_SU7_ru | Информация по SU7 |
| @xiaomiautoclub | Технические дискуссии (FAQ-тред 17455) |
| @xmetaru | Сервис-новости |

**Telethon аккаунт:** @sasha_ikosha (id=8632375143)

### Контакты сервиса (упоминаются на сайте):
- **XMETA** (Санкт-Петербург) — клубный сервис
- **E.N.SERVICE** (E.N.Parts) — запчасти
- **Лантян Электроникс (蓝天电子)** — китайская тех. поддержка

---

## 🛠️ Стек и инструменты

- **Editing:** Pinegrow + VS Code
- **Локальный сервер:** `npx serve .` или browser-sync
- **Backups:** MAX SyncUp → `.tgz`
- **Scraping:** Telethon (требует AmneziaVPN перед запуском!)
- **Сон ноутбука** при питании от сети — ОТКЛЮЧЕН (засыпание ломает Telethon)

---

## 🤝 Двойной workflow модели

- **Claude.ai (этот чат)** — поиск контента, точечные правки, file artifacts, ZIP, аудит
- **Claude Code (локально)** — массовые HTML edits, скрипты, DOCX/PDF чтение, автоматизация

После каждой Claude Code сессии:
1. MAX SyncUp → `.tgz`
2. Отправить в Claude.ai чат для верификации (распаковка, diff)
3. Только потом — финальный ZIP для WinSCP

---

## 📋 Полный список открытых задач

### 🔴 Высокий приоритет (для следующего чата):

1. **Деплой текущего патча** на yu7.site через WinSCP — ZIP уже готов
2. **Проверка дублей обычных видео** — `reply 779`, `reply 366`, черновик `SU7 xiaoai block removal`
3. **Добавить видео «Подлокотник»** в `repair.html` — после решения по дублю #779
4. **Удалить черновик** `SU7 xiaoai block removal`

### 🟡 Средний приоритет:

5. **Yandex.Webmaster + Google Search Console** — переотправить sitemap после деплоя
6. **FAQPage JSON-LD** на топ-5 страниц для rich snippets
7. **Renaming канала V M** в «YU7.site» с правильным handle
8. **4 SKIP-фото мануала** (`retry_skipped.py`) — `#122822, #123652, #127192, ещё одно`

### 🟢 Низкий приоритет:

9. **3 DOCX от Сергея** в `media/reply_27710/29901/28742_*.docx` — сравнить с `xiaomi_yu7_hypertask.html`
10. **138 потерянных медиа** в `xiaomiautoclub_17455` (62 skipped) и `XiaomiEVclub_5358` (76 skipped) — re-download через `fetch_threads.py`

### 🚗 Личные ADAS (Roman, не для сайта):

- Persistent ADAS warnings («Forward collision avoidance is limited» / «Lane assist is limited»)
- Диагноз: физическая разкалибровка сенсоров после транспортировки
- Контакт: 蓝天电子 (Lantian Electronics) — был в процессе

---

## 🎓 Ключевые learnings и грабли

1. **Сон ноута ломает Telethon** → отключить «Sleep when plugged in»
2. **Telegram блок в РФ** → AmneziaVPN перед каждым запуском Telethon
3. **YouTube автоматически делает Shorts** для вертикальных ≤ 3 мин
4. **`file_reference expired`** при долгом fetch_threads → нужен retry_skipped.py
5. **YouTube embed** работает одинаково для Shorts и обычных видео через `youtube.com/embed/{ID}`
6. **Дубликаты при заливке** — проверять перед заливкой нет ли старого `reply_NNN_video`
7. **Координаты в Chrome MCP меняются** после скролла/обновления — каждый раз скриншот для проверки
8. **`og:image` кэшируется Telegram** — для обновления превью добавлять `?v=N` в URL
9. **CSS на сайте уже содержит** `.video-embed`, `.video-embed-frame`, `.video-embed-header`, `.note-warning`, `.note-danger`, `.note-info` — НЕ ДУБЛИРОВАТЬ
10. **`.video-embed-frame` по умолчанию 9:16** — для 16:9 inline стиль `style="aspect-ratio: 16 / 9; max-width: 100%;"`

---

## 📝 Шаблон карточки для новых YouTube-видео

```
Название: [Тема] Xiaomi YU7 (или SU7 — с warning)

Описание:
Краткое описание (1-2 предложения).

[если для SU7] ⚠️ Это инструкция для Xiaomi SU7 (седан). На YU7 компоновка отличается.

Полная информация по [теме] YU7 — на сайте https://yu7.site/[page].html

Источник: канал @XiaomiY7MAX в Telegram (https://t.me/XiaomiY7MAX/POST_ID)
Автор: @AuthorTelegramHandle

#XiaomiYU7 #YU7 #Тема #XiaomiAuto
```

---

## 📊 Статистика по проекту на момент 2026-05-06

- **Страниц на сайте:** 40+ HTML файлов
- **Категорий:** 16/16 заполнены
- **Видео на канале V M:** ~15 (после удаления 6 дублей)
- **Telegram-постов в скрапе:** 3249+ (за 9 дней апрель-май 2026)
- **Treads с FAQ:** 4 основных
- **Реплик в FAQ-треде XiaomiY7MAX/9:** 215

---

## 🚀 С чего начать следующий чат

Скажи Claude:

> «продолжай yu7.site по плану»

Затем сообщи:
1. **Применил ли патч?** (да/нет, какие проблемы при деплое)
2. **ZIP залит на хостинг?**
3. **Готов разбираться с дублями обычных видео?** (`reply 779`, `reply 366`, черновик XiaoAi)

Claude должен:
1. Прочитать этот файл
2. Если деплой не сделан — помочь с деплоем
3. Если деплой готов — пройтись через `youtube.com/shorts/{ID}` для проверки `reply 779/366`, выбрать стратегию по аналогии с карбоном

---

**Версия документа:** 2.0 (после сессии 2026-05-06)
**Автор:** Roman / Herbert Wells (@HerbertWells)
**Поддержка:** Claude (через Anthropic)
