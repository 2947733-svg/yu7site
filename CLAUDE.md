# yu7.site — инструкция для Claude Code

Этот файл читается Claude Code автоматически при работе с проектом yu7.site.

## Расположение и стек

- **Локальный репо:** `C:\claude-test\yu7-digest\site_live\`
- **GitHub:** https://github.com/2947733-svg/yu7site
- **Ветка:** `master` (НЕ main)
- **Стек:** статический HTML + один общий `article.css`, без сборщика
- **Git binary:** `C:\Program Files\Git\bin\git.exe`

## Деплой — АВТОМАТ через cron

**Никаких WinSCP, FTP, ручных заливок файлов через ispmanager.**

Пайплайн:
1. Правка файла локально в `site_live\`
2. `git add ... && git commit -m "..."`
3. `git pull --rebase origin master && git push origin master` - pull ОБЯЗАТЕЛЬНО после коммита и перед пушем: в репо параллельно пушат чат Claude.ai и Takopi, локальная копия часто отстаёт от origin. До коммита pull --rebase не сработает (unstaged changes)
4. Cron на reg.ru каждые 2 минуты делает в `~/www/yu7.site/`:
   `git fetch origin master && git merge --ff-only origin/master`
5. Сайт обновлён за ≤2 мин

После пуша никаких действий на сервере вручную не требуется.

Если push отклонён (rejected, non-fast-forward) - значит pull пропущен: `git pull --rebase origin master`, потом push снова.
Если rebase даёт конфликт ТОЛЬКО в `search-index.json` - не мержить руками:
```
git checkout --ours search-index.json
python -X utf8 C:\claude-test\yu7-digest\regen_search_index.py
git add search-index.json
set GIT_EDITOR=true
git rebase --continue
git push origin master
```

## Перед КАЖДОЙ правкой существующего файла

1. Создать папку `C:\Claude\BackUp\DD_MM_YYYY\` если её нет
2. Скопировать оригинал: `<имя>.bak_<контекст>` (например `tpms.html.bak_pered_lokid78`)
3. Затем править

Новые файлы с нуля бэкапа не требуют.

## ОБЯЗАТЕЛЬНО при добавлении / изменении контента страницы

После правки HTML-файла **всегда перегенерировать `search-index.json`**:
```
C:\Users\HW\AppData\Local\Programs\Python\Python312\python.exe -X utf8 C:\claude-test\yu7-digest\regen_search_index.py
```
- Скрипт собирает индекс по всем страницам сам. Руками `search-index.json` НЕ править никогда - ручные правки затираются следующим запуском и дают конфликты при rebase
- Проверить, что новые ключевые слова попали в индекс: `git grep -c <слово> search-index.json`
- Коммитить вместе с HTML

Без этого новый контент **не будет искаться** на сайте.

## Стиль коммитов

- Латиница, дефисы вместо пробелов
- Пример: `tpms-zamena-datchika-priobresti-u-lokid78`
- Не вставлять переводы строк в `-m`

## КРИТИЧНЫЕ ЗАПРЕТЫ

### НЕ заливать файлы через ispmanager «Менеджер файлов»
Это создаёт untracked-файлы на сервере, которые ломают `git merge --ff-only`.
Симптом в `~/yu7_deploy.log`: `untracked working tree files would be overwritten`.
Только git push.

### НЕ использовать SSH к reg.ru
Адрес `server157.hosting.reg.ru:1500` забанит fail2ban при попытках напрямую.
Whitelist у reg.ru на shared-хостинге невозможен. Для ручных команд на сервере — только ispmanager Shell-клиент в браузере.

### НЕ выдумывать факты про YU7
Любой технический факт (датчики, размеры, меню, артикулы, поставщики, посты #NNNN) — сначала проверить в первоисточнике (PDF мануал, фото, metadata.json), потом писать. Не открыл источник = факта нет. Экстраполяция по аналогии с другими машинами запрещена.

### Меню YU7 — никогда по-русски
Только китайский или английский оригинал + русский в скобках:
`设置 (Settings) → 服务 (Service) → 洗车模式 (Car Wash Mode)`
Если нет фото планшета — попросить Романа сфотографировать, не выдумывать.

## Уточнения у Романа перед нетривиальной правкой

- Какая страница (точный файл)
- Какой старый текст (точная фраза)
- Какой новый текст
- Где взять источник факта

Сразу выполнять только мелочи: опечатки, цвета, одна строка.

## Восстановление после конфликта на сервере

Если в `~/yu7_deploy.log` появилось `untracked working tree files would be overwritten`:

Через ispmanager Shell-клиент:
```bash
cd ~/www/yu7.site
mv <папка> /tmp/<backup>
git checkout -B master origin/master
git status   # должен быть чистый, на master, синхронен с origin/master
```

## Расписание cron на сервере

`*/2 * * * *` — каждые 2 минуты, круглые сутки.
Задаётся в ispmanager → Планировщик → задание → **экспертный режим** (только так можно ввести `*/2`).
Базовый режим даёт только `0 0 * * *` (раз в сутки).

Поля в экспертном режиме:
- Минуты: `*/2`
- Часы: `*`
- Дни месяцев: `*`
- Месяцы: `*`
- Дни недели: `*`

## Авторы и сообщество

- **Владелец сайта:** Roman / Herbert Wells (@Herbert_Wells)
- **Сообщество:** @XiaomiEVclub
- **Источник большинства фактов:** обсуждения в клубе + личный опыт Романа (YU7 Max)

## Что делать когда что-то пошло не так

1. Локальные MCP-серверы зависли → запустить `C:\claude-test\claude-restart.bat`
2. fail2ban забанил IP → ждать 20-30 минут
3. Сайт показывает старый текст после пуша → проверить `cat ~/yu7_deploy.log | tail -10` в ispmanager Shell
4. Cron говорит `Already up to date` но коммиты не приходят → проверить ветку: должна быть `master`, не `main`
