# -*- coding: utf-8 -*-
"""Проверяет уже записанные URL и пишет статус в data/mentions.js.

Текст страницы в карточки не попадает. Новые упоминания не добавляются.
"""

import ssl
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cabinet_logic import CHECKED_LINK_STATUSES, load_mentions, save_mentions

TIMEOUT = 20
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)


def _same_target(left, right):
    return (left or "").rstrip("/").lower() == (right or "").rstrip("/").lower()


def check_url(url):
    req = Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            code = getattr(resp, "status", None) or resp.getcode()
            final = resp.geturl()
            resp.read(256)
        if 200 <= int(code) < 300:
            if _same_target(final, url):
                return "открывается", "код %s" % code
            return "редирект и открытие", "код %s" % code
        return "недоступна", "код %s" % code
    except HTTPError as exc:
        return "недоступна", "код %s" % exc.code
    except URLError as exc:
        reason = getattr(exc, "reason", exc)
        if isinstance(reason, TimeoutError):
            return "недоступна", "таймаут"
        text = str(reason).lower()
        if "timed out" in text or "timeout" in text:
            return "недоступна", "таймаут"
        if isinstance(reason, ssl.SSLError) or "certificate" in text or "ssl" in text:
            return "недоступна", "ошибка сертификата"
        return "недоступна", "запрос не прошел"
    except TimeoutError:
        return "недоступна", "таймаут"
    except Exception:
        return "недоступна", "запрос не прошел"


def main():
    items = load_mentions()
    stamp = date.today().isoformat()
    results = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(check_url, item["url"]): item["id"] for item in items}
        for future in as_completed(futures):
            item_id = futures[future]
            status, reason = future.result()
            if status not in CHECKED_LINK_STATUSES:
                status, reason = "недоступна", "запрос не прошел"
            results[item_id] = (status, reason)
    for item in items:
        status, reason = results[item["id"]]
        item["linkStatus"] = status
        item["linkReason"] = reason
        item["linkCheckedAt"] = stamp
    save_mentions(items)
    tally = {}
    for item in items:
        tally[item["linkStatus"]] = tally.get(item["linkStatus"], 0) + 1
    print("checked", len(items))
    for key in sorted(tally):
        print(key, tally[key])


if __name__ == "__main__":
    main()
