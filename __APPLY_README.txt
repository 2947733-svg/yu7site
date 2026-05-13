КОНТЕНТ-ПАТЧ из FAQ — итерация 2
=================================

ФАЙЛЫ В АРХИВЕ (3):

  keys.html
    + Раздел "Поддерживаемые модели — телефоны Xiaomi и Redmi"
      (24 модели Xiaomi + Redmi для BT и NFC)
    + Раздел "Поддерживаемые модели — часы и браслеты"
      (Mi Band 8 NFC, Mi Band 8 Pro, Watch S3)
    Источники: @XiaomiEVclub #9806, #9868, #10257

  pilot.html
    + Раздел "Ответы на тесты (для справки)"
      (5 тестов с буквенными ответами + предупреждение о версии прошивки)
    Источник: @XiaomiEVclub #18841

  winter.html
    + Раздел "Автоматический подогрев и охлаждение сидений"
      (логика автомата HyperOS)
    Источник: @XiaomiEVclub #30015

ВСЕ ТЕКСТЫ — СТРОГО ИЗ ОРИГИНАЛЬНЫХ ПОСТОВ FAQ.

ПРОВЕРКИ:
  ✓ html-validate: 0 ошибок
  ✓ JSON-LD: вся разметка сохранена, валидна
  ✓ FAQPage на winter.html и keys.html — на месте

КАК ПРИМЕНИТЬ:

  1. Бэкап:
     $ts = Get-Date -Format 'yyyy-MM-dd_HHmm'
     Copy-Item C:\claude-test\yu7-digest\site_live "C:\Claude\BackUp\site_live_before_faq_p2_$ts" -Recurse

  2. Распаковать в C:\claude-test\yu7-digest\site_live\ С ЗАМЕНОЙ.

  3. Локальная проверка:
     cd C:\claude-test\yu7-digest\site_live
     .\predeploy_check.ps1

  4. Деплой через WinSCP — залить 3 HTML.

  5. Визуальная проверка:
     https://yu7.site/keys.html       → раздел "Поддерживаемые модели" (между NFC и Face ID)
     https://yu7.site/pilot.html      → раздел "Ответы на тесты" (внутри "Как активировать")
     https://yu7.site/winter.html     → раздел "Автоматический подогрев..." (между прогревом батареи и зимовкой)

  ВАЖНО: __APPLY_README.txt на хостинг НЕ заливать.
