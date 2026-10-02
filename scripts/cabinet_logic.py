# -*- coding: utf-8 -*-
"""Правила кабинета. Тот же смысл, что у фильтра в index.html."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENTIONS_PATH = ROOT / "data" / "mentions.js"

FILTERS = [
    "Вся лента",
    "О нас написали",
    "СМИ",
    "Документ",
    "Карточка",
    "Вакансия и отзыв",
    "Соцсеть",
    "Свой сайт",
]

LINK_STATUSES = (
    "открывается",
    "редирект и открытие",
    "недоступна",
    "проверка не запускалась",
)

CHECKED_LINK_STATUSES = (
    "открывается",
    "редирект и открытие",
    "недоступна",
)

TONE_STATUSES = ("не размечено", "позитивная", "негативная", "нейтральная")

TONE_MARKERS = {
    "позитивная": "позитив",
    "негативная": "негатив",
    "нейтральная": "нейтрал",
}


def load_mentions(path=None):
    path = Path(path or MENTIONS_PATH)
    text = path.read_text(encoding="utf-8")
    start = text.find("[")
    end = text.rfind("]")
    if start < 0 or end < start:
        raise ValueError("В mentions.js нет массива")
    data = json.loads(text[start : end + 1])
    if not isinstance(data, list):
        raise ValueError("mentions.js должен быть массивом")
    return data


def save_mentions(items, path=None):
    path = Path(path or MENTIONS_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(items, ensure_ascii=False, indent=2)
    path.write_text("window.MENTIONS = " + body + ";\n", encoding="utf-8")


def host(url):
    try:
        from urllib.parse import urlparse

        name = urlparse(url).hostname or ""
        if name.startswith("www."):
            name = name[4:]
        return name
    except Exception:
        return ""


def match(item, current, query):
    if query:
        hay = " ".join(
            [
                item.get("title") or "",
                item.get("frag") or "",
                item.get("type") or "",
                item.get("key") or "",
                item.get("theme") or "",
                host(item.get("url") or ""),
            ]
        ).lower()
        if query.lower() not in hay:
            return False
    if current == "Вся лента":
        return True
    if current == "О нас написали":
        return not item.get("own")
    return item.get("type") == current


def counts(items):
    about = 0
    own_site = 0
    own_tg = 0
    for item in items:
        if item.get("type") == "Свой сайт":
            own_site += 1
        if item.get("own") and item.get("type") == "Соцсеть":
            own_tg += 1
        if not item.get("own"):
            about += 1
    return {"about": about, "own_site": own_site, "own_tg": own_tg, "total": len(items)}


def tone_matches_fragment(item):
    tone = item.get("tone")
    if tone == "не размечено":
        return True
    marker = TONE_MARKERS.get(tone)
    if not marker:
        return False
    return marker in (item.get("frag") or "").lower()


def theme_matches_fragment(item):
    theme = item.get("theme") or ""
    if theme == "не размечено":
        return True
    hay = ((item.get("frag") or "") + " " + (item.get("title") or "")).lower()
    return theme.lower() in hay
