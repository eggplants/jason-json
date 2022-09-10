import json
import re
import ssl
import urllib.request
from datetime import datetime
from http.client import HTTPResponse
from typing import cast

import bs4

from .types import BusinessTime, Data, Shop

ssl._create_default_https_context = ssl._create_unverified_context


def get(url: str) -> bytes | None:
    with urllib.request.urlopen(url) as response:
        res = cast(HTTPResponse, response)
        return res.read() if res.readable() else None


def parse(source: bytes) -> Data:
    bs = bs4.BeautifulSoup(source, features="lxml")
    prefs = bs.select("div.elementor-toggle-item")
    data: Data = {}
    for pref in prefs:
        pref_title = pref.select_one("a.elementor-toggle-title")
        table = pref.select_one("table.table.table-network")
        if pref_title is None or pref_title.string is None or table is None:
            continue
        data[pref_title.string] = _parse_table(table)
    return data


def _parse_table(table: bs4.Tag | None) -> list[Shop]:
    shops: list[Shop] = []
    if table is None:
        return shops

    for row in table.select("tr"):
        first, second, *_ = row.select("td")
        link_a = first.select_one("a")
        address, business_time, *_ = str(second.text).split("営業時間:", 1)
        shop: Shop = {
            "name": _parse_shop_name(link_a),
            "address": address.strip(),
            "link": _parse_shop_link(link_a),
            "business_time": _parse_business_time(business_time),
        }
        shops.append(shop)
    else:
        return shops


def _parse_shop_name(shop_link_a: bs4.Tag | None) -> str | None:
    if shop_link_a is None or shop_link_a.text is None:
        return None
    return shop_link_a.text.strip()


def _parse_shop_link(shop_link_a: bs4.Tag | None) -> str | None:
    if shop_link_a is None:
        return None
    href = shop_link_a.get("href")
    if href is None or isinstance(href, list):
        return None
    return href.strip()


def _parse_business_time(business_time: str) -> BusinessTime | None:
    def _parse_time(time: str) -> datetime:
        return datetime.strptime(time, "%H:%M")

    m = re.match(r"(\d+:\d+)～(\d+:\d+)", business_time)
    if m is None:
        return None

    begin_str, end_str = m.groups()

    zero_time = _parse_time("00:00")
    begin_time = _parse_time(begin_str)
    end_time = _parse_time(end_str)

    return {
        "begin_sec": (begin_time - zero_time).seconds,
        "end_sec": (end_time - zero_time).seconds,
        "duration_sec": (end_time - begin_time).seconds,
        "duration_str": m.group(),
    }


def example_main() -> None:
    URL = "https://jason.co.jp/network/"
    source = get(URL)
    if source is None:
        raise ValueError(f"Failed to fetch source from {URL}")
    data = parse(source)
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    print(json_str)


if __name__ == "__main__":
    example_main()
