from typing import TypedDict

from typed_argparse import TypedArgs


class Args(TypedArgs):
    help: bool
    indent: int | None
    overwrite: bool
    save: bool
    url: str
    version: bool


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
