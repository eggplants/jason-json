from typing import TypedDict


class BusinessTime(TypedDict):
    begin_sec: int
    end_sec: int
    duration_sec: int
    duration_str: str


class Shop(TypedDict):
    name: str | None
    address: str
    link: str | None
    business_time: BusinessTime | None


Data = dict[str, list[Shop]]
