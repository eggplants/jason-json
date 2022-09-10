import urllib.request
from datetime import datetime
import bs4
import json
import re

from typing import TypedDict

class BusinessTime(TypedDict):
  begin_sec: int
  end_sec: int
  duration_sec: int

class Shop(TypedDict):
  name: str | None
  address: str
  link: str | None
  business_time: BusinessTime | None

Shops = list[Shop]

Data = dict[str, list[Shops]]

def get(url: str) -> str:
  html = urllib.request.urlopen(url)

def parse(source: str) -> Data:
  bs = bs4.BeautifulSoup(source)
  prefs = bs.select("div[class='elementor-toggle-item']")
  json_dict: Data = {}
  for pref in prefs:
    pref_name = pref.select_one("div[class='elementor-toggle-title']")
    table = pref.select_one("table[class='table table-network']")
    json_dict[pref_name] = parse_table(table)

def parse_table(table: bs4.Tag | None) -> list[Shop]:
  shops: Shops = []
  if table is None:
    return shops

  for row in table.select("tr"):
    first, second, *_ = row.select("td")
    link_a = first.select_one("a"),
    address, business_time = str(second.string).split("営業時間:", 1)

    shop: Shop = {
      "link": None if link_a is None else link_a.href,
      "name": first.string,
      "business_time": business_time,
      "address": address,
      "business_time": parse_business_time(business_time)
    }
    shops.append(shop)
  else:
    return shops

def parse_business_time(business_time: str) -> BusinessTime | None:
  m = re.match(r'^(\d\d:\d\d)〜(\d\d:\d\d)', business_time)
  if m is None:
    return None

  begin_str, end_str = business_time.groups

  zero_time = parse_time("00:00")
  begin_time = parse_time(begin_str)
  end_time = parse_time(end_str)

  return {
    "begin_sec": (begin_time - zero_time).seconds,
    "end_sec": (end_time - zero_time).seconds,
    "duration_sec": (end_time - begin_time).seconds,
  }

def parse_time(time: str) -> datetime:
  return datetime.strptime(time, "%H:%M")



def main():
  source = get("https://jason.co.jp/network/")
  data = parse(source)
  json_str = json.dumps(data, indent=2)
  print(json_str)

if __name__ == "__main__":
  main()
