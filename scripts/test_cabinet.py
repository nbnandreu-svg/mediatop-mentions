# -*- coding: utf-8 -*-
"""Проверки данных кабинета. Запуск: python scripts/test_cabinet.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cabinet_logic import (  # noqa: E402
    CHECKED_LINK_STATUSES,
    FILTERS,
    TONE_STATUSES,
    counts,
    load_mentions,
    match,
    theme_matches_fragment,
    tone_matches_fragment,
)

ROOT = Path(__file__).resolve().parents[1]

EXPECTED = [
    ("m01", "СМИ", False, "22 августа 2025", "https://www.cnews.ru/news/line/2025-08-22_pravitelstvo_rossii_opredelilo", "Распоряжение № 2235-р, единственный поставщик Минсельхоза."),
    ("m02", "СМИ", False, "14 октября 2024", "https://www.comnews.ru/content/235684/2024-10-14/2024-w42/1008/minselkhoz-vysadil-10-gis-agropromcifru", "Десять ГИС, кроме «Зерна»."),
    ("m03", "СМИ", False, "20 мая 2026", "https://www.comnews.ru/content/245376/2026-05-20/2026-w21/1007/edinaya-cifrovaya-platforma-minselkhoza-stala-pozdneurozhaynoy", "Первая очередь ЕЦП 2 марта 2026 года."),
    ("m04", "СМИ", False, "22 мая, год не указан", "https://www.interfax.ru/russia/1091254", "Чебунина про приложение ЕЦП до конца 2026 года."),
    ("m05", "СМИ", False, "дата на странице не видна", "https://www.osp.ru/resources/releases?rid=54977", "Пресс-релиз о соглашении с Arenadata. Это их текст на чужой площадке."),
    ("m06", "Документ", False, "16 мая 2026", "https://rulaws.ru/goverment/Rasporyazhenie-Pravitelstva-RF-ot-16.05.2026-N-1130-r/", "Полное имя, без короткого ключа."),
    ("m07", "Карточка", False, "дата не снята", "https://www.tadviser.ru/index.php/%D0%9A%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F:%D0%90%D0%B3%D1%80%D0%BE%D0%BF%D1%80%D0%BE%D0%BC%D1%86%D0%B8%D1%84%D1%80%D0%B0", "Имя есть в выдаче. Страница не открылась."),
    ("m08", "Карточка", False, "дата не снята", "https://companies.rbc.ru/id/1237700386417-nao-ao-agropromtsifra/", "Карточка юрлица."),
    ("m09", "Карточка", False, "дата не снята", "https://saby.ru/profile/7708420238-770801001", "Карточка по ИНН."),
    ("m10", "Карточка", False, "дата не снята", "https://firmoteka.ru/7708420238", "Карточка по ИНН."),
    ("m11", "Карточка", False, "дата не снята", "https://spark-interfax.ru/moskva-krasnoselski/ao-agropromtsifra-inn-7708420238-ogrn-1237700386417-fd45fc0735e55b9de053259aa8c03522", "Карточка юрлица."),
    ("m12", "Карточка", False, "дата не снята", "https://www.rusprofile.ru/id/1237700386417", "Карточка юрлица."),
    ("m13", "Карточка", False, "дата не снята", "https://specagro.ru/fgis/digital_apk", "Карточка контакта."),
    ("m14", "Вакансия и отзыв", False, "сентябрь 2026", "https://dreamjob.ru/employers/3345009", "13 отзывов, оценка 4,5. Свежий отзыв за сентябрь 2026."),
    ("m15", "Вакансия и отзыв", False, "дата не снята", "http://hh.ru/employer/10216642?hhtmFrom=vacancy_search_list", "Карточка работодателя."),
    ("m16", "Вакансия и отзыв", False, "дата не снята", "https://hh.ru/vacancy/136938629", "Вакансия."),
    ("m17", "Вакансия и отзыв", False, "дата не снята", "https://hh.ru/vacancy/133919799", "Вакансия."),
    ("m18", "Соцсеть", True, "дата не снята", "https://t.me/agropromcifra", "Свой канал, 1031 подписчик. Посты не листались."),
    ("m19", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/", "Ключ на странице своего сайта."),
    ("m20", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/service-strategy", "Ключ на странице своего сайта."),
    ("m21", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/edu", "Ключ на странице своего сайта."),
    ("m22", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/contacts", "Ключ на странице своего сайта."),
    ("m23", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/head-of-digital-transformation-2025", "Ключ на странице своего сайта."),
    ("m24", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/news/otvety-na-chasto-zadavayemye-voprosy-po-etsp", "Ключ на странице своего сайта."),
    ("m25", "Свой сайт", True, "дата не снята", "https://agropromcifra.ru/news/pravitelstvo-rf-opredelilo-ao-agropromtsifra-edinstvennym-postavshchikom-dlya-tsifrovoy-transformatsii-minselkhoza-rossii", "Ключ на странице своего сайта."),
]


class CabinetDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.items = load_mentions()

    def test_exact_collection(self):
        self.assertEqual(len(self.items), 25)
        self.assertEqual(len(EXPECTED), 25)
        for item, expected in zip(self.items, EXPECTED):
            item_id, kind, own, day, url, frag = expected
            self.assertEqual(item["id"], item_id)
            self.assertEqual(item["type"], kind)
            self.assertEqual(item["own"], own)
            self.assertEqual(item["date"], day)
            self.assertEqual(item["url"], url)
            self.assertEqual(item["frag"], frag)
            self.assertTrue(item.get("title"))
            self.assertTrue(item.get("key"))

    def test_counts(self):
        got = counts(self.items)
        self.assertEqual(got["about"], 17)
        self.assertEqual(got["own_site"], 7)
        self.assertEqual(got["own_tg"], 1)
        self.assertEqual(got["total"], 25)

    def test_about_filter_excludes_own(self):
        rows = [item for item in self.items if match(item, "О нас написали", "")]
        self.assertEqual(len(rows), 17)
        self.assertTrue(all(not item["own"] for item in rows))
        self.assertTrue(all(item["type"] != "Свой сайт" for item in rows))

    def test_type_filters(self):
        expected = {
            "СМИ": 5,
            "Документ": 1,
            "Карточка": 7,
            "Вакансия и отзыв": 4,
            "Соцсеть": 1,
            "Свой сайт": 7,
            "Вся лента": 25,
        }
        for name, size in expected.items():
            rows = [item for item in self.items if match(item, name, "")]
            self.assertEqual(len(rows), size, name)
        self.assertEqual(FILTERS[0], "Вся лента")

    def test_empty_search(self):
        rows = [item for item in self.items if match(item, "Вся лента", "qqqq-нет-такой-строки")]
        self.assertEqual(rows, [])

    def test_search_hit(self):
        rows = [item for item in self.items if match(item, "Вся лента", "cnews")]
        self.assertEqual([item["id"] for item in rows], ["m01"])

    def test_required_fields_and_link_status(self):
        for item in self.items:
            self.assertTrue(item.get("url"))
            self.assertTrue(item.get("type"))
            self.assertTrue(item.get("frag"))
            self.assertIn(item.get("linkStatus"), CHECKED_LINK_STATUSES)
            self.assertTrue(item.get("linkReason"))
            self.assertIn(item.get("tone"), TONE_STATUSES)
            self.assertTrue(tone_matches_fragment(item))
            self.assertTrue(item.get("theme"))
            self.assertTrue(theme_matches_fragment(item))
            self.assertTrue((item.get("pullText") or "").strip(), item["id"])

    def test_page_does_not_hardcode_counts(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotIn("сайта 7", html)
        self.assertNotIn(">17<", html)
        self.assertIn('id="n-about"', html)
        self.assertIn('id="n-site"', html)
        self.assertIn('id="n-tg"', html)
        self.assertIn("data/mentions.js", html)
        self.assertIn('var current = "Вся лента"', html)


if __name__ == "__main__":
    unittest.main(verbosity=1)
