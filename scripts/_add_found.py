# -*- coding: utf-8 -*-
"""Добавляет упоминания, страницы которых открыты и содержат имя компании."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cabinet_logic import load_mentions, save_mentions

NEW = [
    {
        "id": "m26",
        "type": "СМИ",
        "own": False,
        "date": "19 мая 2026",
        "title": "AK&M",
        "url": "https://www.akm.ru/news/agropromtsifra_vnov_opredelena_edinstvennym_postavshchikom_dlya_tsifrovoy_transformatsii_minselkhoza/",
        "frag": "Агропромцифра вновь определена единственным поставщиком Минсельхоза на 2026-2027 годы.",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "единственный поставщик",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "АО «Агропромышленный центр цифровизации» (Агропромцифра) определено единственным поставщиком закупок Минсельхоза России в 2026-2027 годах для развития и эксплуатации государственных информационных систем.",
        "pullLocked": True,
    },
    {
        "id": "m27",
        "type": "СМИ",
        "own": False,
        "date": "20 мая 2026",
        "title": "Milknews",
        "url": "https://milknews.ru/index/agropromcifra-apk-postavschikk.html",
        "frag": "Агропромцифра вновь определена единственным поставщиком Минсельхоза на 2026-2027 годы.",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "единственный поставщик",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "Чистая прибыль АО «Агропромышленный центр цифровизации» (Агропромцифра) по РСБУ за 2025 год увеличилась в 6 раз до 237,4 млн руб. Выручка выросла до 1,8 млрд руб.",
        "pullLocked": True,
    },
    {
        "id": "m28",
        "type": "СМИ",
        "own": False,
        "date": "22 мая 2026",
        "title": "ict-online",
        "url": "https://ict-online.ru/news/Agropromtsifra-poluchila-klyuchevyye-IT-zakazy-Minsel-khoza-na-2026-2027-gody-326989",
        "frag": "«Агропромцифра» получила ключевые ИТ-заказы Минсельхоза на 2026-2027 годы.",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "единственный поставщик",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "Распоряжением № 1130-р от 16 мая 2026 года АО «Агропромышленный центр цифровизации» («Агропромцифра») определено единственным поставщиком Минсельхоза на 2026-2027 годы.",
        "pullLocked": True,
    },
    {
        "id": "m29",
        "type": "СМИ",
        "own": False,
        "date": "3 августа 2026",
        "title": "ComNews",
        "url": "https://www.comnews.ru/digital-economy/content/246704/2026-08-03/2026-w32/1012/agropromcifra-i-smart-tekhnologii-invest-zapustili-platformu-dlya-prognozirovaniya-bioriskov-predpriyatiyakh-apk",
        "frag": "«Агропромцифра» и «Смарт Технологии Инвест» запустили пилот «БиоПульс».",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "БиоПульс",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "«Агропромцифра» и «Смарт Технологии Инвест» запустили пилотный проект по контролю биобезопасности в животноводстве. Платформа называется «БиоПульс».",
        "pullLocked": True,
    },
    {
        "id": "m30",
        "type": "СМИ",
        "own": False,
        "date": "1 октября 2026",
        "title": "CNews",
        "url": "https://www.cnews.ru/news/line/2026-10-01_tsifrovaya_platforma_atlas",
        "frag": "«Агропромцифра» и МГИМО представили платформу «Атлас мировых аграрных рынков».",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "Атлас",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "АО «Агропромцифра» и МГИМО представили рабочую версию цифровой платформы «Атлас мировых аграрных рынков».",
        "pullLocked": True,
    },
    {
        "id": "m31",
        "type": "Карточка",
        "own": False,
        "date": "дата не снята",
        "title": "ComNews, кто есть кто",
        "url": "https://whoiswho.comnews.ru/person/67339/chebunina-olga-aleksandrovna",
        "frag": "Карточка Ольги Чебуниной: генеральный директор АО «Агропромцифра».",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "не размечено",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "Генеральный директор АО «Агропромцифра», заместитель председателя ИЦК «Сельское хозяйство».",
        "pullLocked": True,
    },
    {
        "id": "m32",
        "type": "Карточка",
        "own": False,
        "date": "дата не снята",
        "title": "Каталог AgroExpo",
        "url": "https://catalog.iagri-expo.com/companies/company/142154-agropromtsifra.html",
        "frag": "Карточка участника: ИТ-решения, заказная разработка, обучение, кибербезопасность.",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "не размечено",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "АО «Агропромцифра». Телефон +7 (495) 120-39-55, адрес: Москва, ул. Садовая-Спасская, д. 11/1.",
        "pullLocked": True,
    },
    {
        "id": "m33",
        "type": "Свой сайт",
        "own": True,
        "date": "дата не снята",
        "title": "Интервью РБК на Зерновом форуме",
        "url": "https://agropromcifra.ru/news/tsifrovizatsiya-v-zernovoy-otrasli-eksklyuzivnoye-intervyu-rbk-olgi-chebuninoy-",
        "frag": "Новость своего сайта: интервью Ольги Чебуниной РБК на Зерновом форуме.",
        "key": "агропромцифра",
        "tone": "не размечено",
        "theme": "не размечено",
        "linkStatus": "открывается",
        "linkReason": "код 200",
        "linkCheckedAt": "2026-10-02",
        "pullText": "На полях Зернового форума генеральный директор АО «Агропромцифра» Ольга Чебунина в видеоинтервью РБК рассказала о цифровизации агропромышленного комплекса.",
        "pullLocked": True,
    },
]


def main():
    items = load_mentions()
    have = {item["url"] for item in items}
    added = 0
    for row in NEW:
        if row["url"] in have:
            continue
        items.append(row)
        added += 1
    save_mentions(items)
    print("total", len(items), "added", added)


if __name__ == "__main__":
    main()
