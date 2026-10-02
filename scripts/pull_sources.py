# -*- coding: utf-8 -*-
"""Снимает со страницы короткий фрагмент вокруг ключа. Новых карточек не создает."""

import re
import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from html import unescape
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cabinet_logic import load_mentions, save_mentions

TIMEOUT = 20
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)
KEYS = (
    "агропромцифр",
    "agropromcifra",
    "agropromtsifra",
    "агропромышленный центр цифровизации",
    "7708420238",
)


CUTS = (
    "Чтобы сайт",
    "cookies",
    "cookie",
    "Главная Новости",
    "Перейти к основному",
    "href=",
    "data-type",
    "data-design",
    "-->",
    "Download",
    "Обновите браузер",
    "Компания месяца",
)


def _visible(raw):
    text = raw.decode("utf-8", "replace")
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r'\s*(?:href|class|id|data-[\w-]+)\s*=\s*"[^"]*"', " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _window(text, at):
    back_from = max(0, at - 80)
    back = text[back_from:at]
    dot = max(back.rfind(". "), back.rfind("! "), back.rfind("? "))
    start = back_from + dot + 2 if dot >= 0 else max(0, at - 24)
    end = min(len(text), at + 190)
    chunk = text[start:end]
    low = chunk.lower()
    for cut in CUTS:
        pos = low.find(cut.lower())
        if pos > 40:
            chunk = chunk[:pos]
    chunk = re.sub(r"<[^>]+>", " ", chunk)
    chunk = chunk.replace("\\n", " ").replace('\\"', '"')
    chunk = re.sub(r"\s+", " ", chunk).strip(" -|>")
    if start > 0 and chunk:
        chunk = "…" + chunk
    return chunk.strip()


def _score(chunk):
    low = chunk.lower()
    score = min(len(chunk), 220)
    for bad in ("href", "cookie", "меню", "подписка", "class=", "data-", "download", "schema.org", "metadata", "{\"@", "\\\"@"):
        if bad in low:
            score -= 120
    if "«" in chunk or "единственн" in low:
        score += 20
    return score


def _excerpt(text):
    low = text.lower()
    spots = []
    for key in KEYS:
        start = 0
        while True:
            at = low.find(key, start)
            if at < 0:
                break
            spots.append(at)
            start = at + len(key)
    best = ""
    best_score = -10**9
    for at in spots:
        chunk = _window(text, at)
        score = _score(chunk)
        if score > best_score:
            best = chunk
            best_score = score
    if best_score < 40:
        return ""
    return best


def pull_url(url):
    req = Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "ru,en;q=0.8",
        },
    )
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            code = int(getattr(resp, "status", None) or resp.getcode())
            final = resp.geturl()
            raw = resp.read(400000)
        if not (200 <= code < 300):
            return "недоступна", "код %s" % code, ""
        excerpt = _excerpt(_visible(raw))
        same = final.rstrip("/").lower() == url.rstrip("/").lower()
        opened = "открывается" if same else "редирект и открытие"
        if excerpt:
            return opened, "код %s" % code, excerpt
        return opened, "код %s, ключ в ответе не найден" % code, ""
    except HTTPError as exc:
        if exc.code in (401, 403, 429):
            return "скрипт не прочитал", "код %s" % exc.code, ""
        return "недоступна", "код %s" % exc.code, ""
    except URLError as exc:
        reason = getattr(exc, "reason", exc)
        text = str(reason).lower()
        if isinstance(reason, TimeoutError) or "timed out" in text or "timeout" in text:
            return "недоступна", "таймаут", ""
        if isinstance(reason, ssl.SSLError) or "certificate" in text or "ssl" in text:
            return "недоступна", "ошибка сертификата", ""
        return "недоступна", "запрос не прошел", ""
    except TimeoutError:
        return "недоступна", "таймаут", ""
    except Exception:
        return "недоступна", "запрос не прошел", ""


def main():
    items = load_mentions()
    stamp = date.today().isoformat()
    results = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(pull_url, item["url"]): item["id"] for item in items}
        for future in as_completed(futures):
            results[futures[future]] = future.result()
    lines = []
    for item in items:
        if item.get("pullLocked"):
            continue
        status, reason, excerpt = results[item["id"]]
        item["linkStatus"] = status
        item["linkReason"] = reason
        item["linkCheckedAt"] = stamp
        item["pullText"] = excerpt
        lines.append("%s | %s | %s | %s" % (item["id"], item["title"], status, "да" if excerpt else "нет"))
    save_mentions(items)
    report = "\n".join(lines)
    open(r"C:\Users\Admin\Desktop\mediatop-mentions\docs\_pull_report.txt", "w", encoding="utf-8").write(report)
    print("wrote", len(items))


if __name__ == "__main__":
    main()
