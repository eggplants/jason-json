"""Type definitions for jason_json."""

from __future__ import annotations

import argparse
from pathlib import Path  # noqa: TC003
from shutil import get_terminal_size
from typing import TypedDict

from tap import Tap

from . import __version__


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


class Args(Tap):
    """Jason (https://jason.co.jp) JSON Builder."""

    indent: int = 2
    overwrite: bool = False
    save: Path | None = None  # type: ignore[assignment]
    url: str = "https://jason.co.jp/network"
    version: bool = False

    def configure(self) -> None:
        """Configure arguments."""
        self.formatter_class = lambda prog: CustomFormatter(
            prog,
            width=get_terminal_size(fallback=(120, 50)).columns,
            max_help_position=25,
        )
        self.add_argument("-i", "--indent", help="number of indentation spaces in json")
        self.add_argument(
            "-O",
            "--overwrite",
            help="overwrite if save path already exists",
        )
        self.add_argument("-s", "--save", help="save json to given path")
        self.add_argument("-u", "--url", help="target url")
        self.add_argument(
            "-V",
            "--version",
            action="version",
            version=__version__,
            help="show program's version number and exit",
        )


class BusinessTime(TypedDict):
    """Jason business time."""

    begin_sec: int
    end_sec: int
    duration_sec: int
    duration_str: str


class Shop(TypedDict):
    """Jason shop information."""

    name: str | None
    address: str
    link: str | None
    business_time: BusinessTime | None


Data = dict[str, list[Shop]]

__all__ = ("Args", "BusinessTime", "Data", "Shop")
