#!/usr/bin/env python3
"""Обновляет поисковый индекс и якоря в HTML. Запуск: python tools/regen_search_index.py."""

import json
import re
from hashlib import blake2s
from html.parser import HTMLParser
from pathlib import Path

SITE_DIR = Path(__file__).resolve().parent.parent

PAGES = [
    "voice-commands.html", "no-power.html", "xiaomi_yu7_hypertask.html",
    "charging-station.html", "adapters.html", "home220.html", "v2l.html",
    "winter.html", "soc-range.html", "battery-key.html", "apps.html",
    "language.html", "china-phone.html", "wheels-specs.html", "tpms.html",
    "jack-mode.html", "alignment.html", "order-china.html", "master-account.html",
    "maintenance.html", "insurance.html", "service.html", "ota.html",
    "carplay.html", "cncap.html", "detailing.html", "docs.html",
    "activation.html", "keys.html", "sentry.html", "pilot.html",
    "telematics.html", "repair.html", "reviews.html",
    # SEO-страницы под топ-запросы (добавлены 2026-04-27)
    "prices.html", "range-real.html", "vs-tesla.html", "reviews-owners.html",
    "faq.html"
]

# Служебные страницы, которые не индексируются никогда.
EXCLUDE_PAGES = {"index.html"}
EXCLUDE_PREFIXES = ("yandex_", "googlea", "google")


def discover_pages():
    """
    PAGES задаёт порядок для уже существующих страниц (стабильный diff индекса),
    все остальные *.html из SITE_DIR добавляются автоматически в конец.
    Раньше список был жёстким, и новые страницы (climate, audio, cargo, lights и др.)
    в поиск не попадали вообще.
    """
    known = [p for p in PAGES if (SITE_DIR / p).exists()]
    extra = sorted(
        p.name for p in SITE_DIR.glob("*.html")
        if p.name not in PAGES
        and p.name not in EXCLUDE_PAGES
        and not p.name.startswith(EXCLUDE_PREFIXES)
    )
    return known + extra


VOID_TAGS = set("area base br col embed hr img input link meta param source track wbr".split())
SKIP_TAGS = {"script", "style", "noscript", "header", "footer", "nav", "template"}
HEADINGS = set("h1 h2 h3 h4 h5 h6".split())
BLOCK_TAGS = HEADINGS | set("p li tr dt dd summary figcaption blockquote pre div".split())
JUMP_STYLE = '<style id="search-jump-style">:target{scroll-margin-top:76px}</style>'
DETAILS_JUMP = '''<script id="search-jump-details">
(function () {
    function openAnswer() {
        const target = document.getElementById(location.hash.slice(1));
        const answer = target && target.closest('details');
        if (answer && !answer.open) {
            answer.open = true;
            target.scrollIntoView();
        }
    }
    window.addEventListener('hashchange', openAnswer);
    openAnswer();
})();
</script>'''
APK_TERMS = ('Скачать Xiaomi Auto на русском. Xiaomi Auto 2.10.1 v4 на русском. '
             'Бесплатный русский APK для Android. xiaomi-auto-2.10.1-ru-v4.apk')
PREFERRED_ANCHORS = {
    "apps.html": ("xiaomi-auto", APK_TERMS),
    "master-account.html": ("download", APK_TERMS),
}


def utf16_len(text):
    """Смещения для String.slice() в браузере."""
    return len(text.encode("utf-16-le")) // 2


class ArticleTextExtractor(HTMLParser):
    """Пишет видимый текст и диапазоны абзацев в том же порядке, что в HTML."""

    def __init__(self, html):
        super().__init__()
        self.html = html
        self.article_only = bool(re.search(r"<article\b", html, re.I))
        self.line_starts = [0, *(m.end() for m in re.finditer("\n", html))]
        self.stack = []
        self.parts = []
        self.length = 0
        self.blocks = []
        self.ids = set()
        self.insertions = []
        self.feed(html)
        self.close()
        while self.stack:
            self.finish(self.stack.pop())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        anchor = attrs.get("id")
        if anchor:
            self.ids.add(anchor)
        if tag in VOID_TAGS:
            return
        parent = self.stack[-1] if self.stack else None
        blocked = (parent is not None and parent["blocked"]) or tag in SKIP_TAGS
        blocked = blocked or "hidden" in attrs or attrs.get("aria-hidden") == "true"
        blocked = blocked or bool(re.search(r"(?:^|;)\s*display\s*:\s*none\b", attrs.get("style") or "", re.I))
        root = "article" if self.article_only else "body"
        visible = not blocked and (tag == root or (parent is not None and parent["visible"]))
        if visible and (tag in BLOCK_TAGS or anchor) and parent is not None:
            parent["nested"] = True
        line, column = self.getpos()
        self.stack.append({
            "tag": tag,
            "anchor": anchor,
            "blocked": blocked,
            "visible": visible,
            "nested": False,
            "part": len(self.parts),
            "position": self.line_starts[line - 1] + column,
        })

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                while len(self.stack) > i:
                    self.finish(self.stack.pop())
                break
            if tag not in BLOCK_TAGS and tag not in {"body", "article", "section", "main", "details",
                                                    "thead", "tbody", "table", "ul", "ol", "dl"}:
                # Обычные строчные элементы всегда закрываются над своим блоком.
                if self.stack[i]["tag"] in BLOCK_TAGS:
                    break

    def handle_data(self, data):
        if self.stack and self.stack[-1]["visible"]:
            value = re.sub(r"\s+", " ", data).strip()
            if value:
                self.add_text(value)

    def add_text(self, value):
        start = self.length + bool(self.parts)
        self.length = start + utf16_len(value)
        self.parts.append((value, start, self.length))
        return start, self.length

    def finish(self, node):
        first = node["part"]
        if not node["visible"] or first == len(self.parts):
            return
        tag = node["tag"]
        if not node["anchor"] and (tag not in BLOCK_TAGS or (tag == "div" and node["nested"])):
            return
        start, end = self.parts[first][1], self.parts[-1][2]
        if end - start < 2 or (tag == "div" and end - start > 2600):
            return
        excerpt = " ".join(value for value, _, _ in self.parts[first:len(self.parts)])
        self.blocks.append((node["position"], tag, node["anchor"], start, end, excerpt))

    def anchors(self):
        ranges = []
        first_heading = None
        for position, tag, anchor, start, end, excerpt in sorted(self.blocks):
            if not anchor:
                digest = blake2s(excerpt.encode(), digest_size=5).hexdigest()
                base = f"search-{digest}"
                anchor = base
                suffix = 2
                while anchor in self.ids:
                    anchor = f"{base}-{suffix}"
                    suffix += 1
                self.ids.add(anchor)
                match = re.match(r"<\s*[\w:-]+", self.html[position:])
                self.insertions.append((position + match.end(), f' id="{anchor}"'))
            ranges.append([anchor, start, end])
            if tag == "h1" and first_heading is None:
                first_heading = anchor
        return ranges, first_heading or (ranges[0][0] if ranges else None)

    @property
    def text(self):
        return " ".join(value for value, _, _ in self.parts)

    def markup(self):
        if JUMP_STYLE not in self.html:
            end_head = re.search(r"</head\s*>", self.html, re.I)
            if end_head:
                self.insertions.append((end_head.start(), JUMP_STYLE + "\n"))
        if re.search(r"<details\b", self.html, re.I) and 'id="search-jump-details"' not in self.html:
            end_body = re.search(r"</body\s*>", self.html, re.I)
            if end_body:
                self.insertions.append((end_body.start(), DETAILS_JUMP + "\n"))
        parts = []
        cursor = 0
        for position, content in sorted(self.insertions):
            parts.extend((self.html[cursor:position], content))
            cursor = position
        return "".join(parts) + self.html[cursor:]


def voice_blocks(html):
    pattern = r"const\s+CATEGORIES\s*=\s*\{(.*?)\n\s*\};\s*const\s+COMMANDS\s*=\s*\[(.*?)\n\s*\];"
    match = re.search(pattern, html, re.S)
    if not match:
        return
    for key, data in re.findall(r"(?m)^\s*(\w+)\s*:\s*\{([^\n]+?)\}", match[1]):
        values = re.findall(r"\b(?:name|note)\s*:\s*'([^']+)'", data)
        if values:
            yield f"search-voice-{key}", " ".join(values)
    for data in re.findall(r"(?m)^\s*\{([^\n]+?)\}", match[2]):
        values = dict(re.findall(r"\b(zh|translit|ru)\s*:\s*'([^']+)'", data))
        if "zh" in values:
            key = "-".join(f"{ord(char):x}" for char in values["zh"])
            yield f"search-cmd-{key}", " ".join(values.values())


def replace_atomically(path, data):
    if path.exists() and path.read_bytes() == data:
        return
    temp = path.with_name(path.name + ".tmp")
    temp.write_bytes(data)
    temp.replace(path)


def index_page(path):
    raw = path.read_bytes()
    html = raw.decode("utf-8").replace("\r\n", "\n")
    ext = ArticleTextExtractor(html)
    ranges, default = ext.anchors()
    if not ranges:
        raise ValueError(f"{path.name}: no searchable paragraphs")
    if path.name == "voice-commands.html":
        for anchor, value in voice_blocks(html):
            start, end = ext.add_text(value)
            ranges.append([anchor, start, end])
    if path.name in PREFERRED_ANCHORS:
        anchor, terms = PREFERRED_ANCHORS[path.name]
        if anchor not in ext.ids:
            raise ValueError(f"{path.name}: missing #{anchor}")
        start, end = ext.add_text(terms)
        ranges.append([anchor, start, end, 1])
    url = "/" + path.name
    markup = ext.markup()
    if b"\r\n" in raw:
        markup = markup.replace("\n", "\r\n")
    return {
        "url": url,
        "title": extract_title(html),
        "meta": extract_short_meta(extract_meta(html), url),
        "text": ext.text,
        "anchor": default,
        "blocks": ranges,
    }, markup.encode("utf-8")


def extract_meta(html, name="description"):
    """Достаёт content из <meta name="X" content="Y">"""
    pattern = rf'<meta\s+name=["\']{name}["\']\s+content=["\']([^"\']+)["\']'
    m = re.search(pattern, html, re.IGNORECASE)
    return m.group(1) if m else ""


def extract_title(html):
    """Достаёт <title> и убирает суффикс ' · YU7.site' если есть"""
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return ""
    title = m.group(1).strip()
    title = re.sub(r"\s*[·•]\s*YU7\.site\s*$", "", title)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


# Короткая meta для каждой страницы (как было в первоначальном индексе)
SHORT_META = {
    "/voice-commands.html": "43 команды с TTS",
    "/no-power.html": "разрядка 12В батареи, экстренная разблокировка",
    "/xiaomi_yu7_hypertask.html": "автоматизация через сценарии",
    "/charging-station.html": "пошагово, провода, ошибки",
    "/adapters.html": "GB/T → CCS2, типы и цены",
    "/home220.html": "медленная зарядка дома, подключение",
    "/v2l.html": "розетка в авто, кабели, ограничения",
    "/winter.html": "запас хода, прогрев, советы",
    "/soc-range.html": "ёмкость, циклы, прогноз ресурса",
    "/battery-key.html": "когда менять, какая нужна",
    "/apps.html": "Скачать Xiaomi Auto на русском, YouTube и навигация",
    "/language.html": "английский интерфейс, китайские пункты",
    "/china-phone.html": "симка, тарифы, eSender",
    "/wheels-specs.html": "размеры, давление, балансировка",
    "/tpms.html": "сброс, замена, нюансы",
    "/jack-mode.html": "как включить, пневмоподвеска",
    "/alignment.html": "когда и где делать, цены",
    "/order-china.html": "процесс, риски, утильсбор",
    "/master-account.html": "Скачать Xiaomi Auto на русском, передача и семейный доступ",
    "/maintenance.html": "что и когда менять, цены",
    "/insurance.html": "тарифы, нюансы, документы",
    "/service.html": "что делают, как записаться",
    "/ota.html": "через сервис, через раздачу интернета",
    "/carplay.html": "как подключить, ограничения",
    "/cncap.html": "что протестировано, результаты",
    "/detailing.html": "плёнка, керамика, защита салона",
    "/docs.html": "руководства, мануалы, FAQ",
    "/activation.html": "что сделать сразу после получения",
    "/keys.html": "BT-брелок, NFC-карта, Face ID",
    "/sentry.html": "запись камер, расход батареи",
    "/pilot.html": "LCC, Pilot Assistant, NOA, активация",
    "/telematics.html": "восстановление связи, впайка RU SIM, eSIM",
    "/repair.html": "запчасти, кузовной, гарантийные кейсы",
    "/reviews.html": "видео-обзоры из YouTube и Telegram",
    "/prices.html": "RWD, Pro, Max — цены в Китае и РФ",
    "/range-real.html": "тесты на трассе, в городе, зимой",
    "/vs-tesla.html": "сравнение с Tesla Model Y",
    "/reviews-owners.html": "плюсы, минусы, типичные болячки"
}


def extract_short_meta(meta_desc, page_url):
    """Короткая meta из словаря SHORT_META; если страницы нет — первые 60 символов."""
    return SHORT_META.get(page_url, meta_desc[:60] if meta_desc else "")


def main():
    pages = []
    markup = []
    for name in discover_pages():
        path = SITE_DIR / name
        entry, html = index_page(path)
        pages.append(entry)
        markup.append((path, html))

    for path, html in markup:
        replace_atomically(path, html)
    index = json.dumps(pages, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    replace_atomically(SITE_DIR / "search-index.json", index)
    print(f"OK: {len(pages)} страниц, {sum(len(page['blocks']) for page in pages)} ссылок, {len(index):,} байт")


if __name__ == "__main__":
    main()
