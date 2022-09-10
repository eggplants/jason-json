import argparse
import json
import os
import ssl
import sys
from shutil import get_terminal_size

from . import __version__
from .utils import get, parse

ssl._create_default_https_context = ssl._create_unverified_context


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def check_path(v: str) -> str:
    if os.path.isdir(v):
        raise argparse.ArgumentTypeError(f"'{v}' already exists as a directory.")
    return v


def check_natural(v: str) -> int:
    v_int = int(v)
    if v_int < 0:
        raise argparse.ArgumentTypeError(f"'{v}' should be natural (>=0).")
    return v_int


def parse_args() -> argparse.Namespace:
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=(
            lambda prog: CustomFormatter(
                prog,
                **{
                    "width": get_terminal_size(fallback=(120, 50)).columns,
                    "max_help_position": 25,
                },
            )
        ),
        description="Jason (jason.co.jp) JSON Builder",
    )
    parser.add_argument(
        "-O",
        "--overwrite",
        action="store_true",
        help="overwrite if save path already exists",
    )
    parser.add_argument(
        "-i",
        "--indent",
        metavar="NAT",
        type=check_natural,
        help="indent json",
    )
    parser.add_argument(
        "-s",
        "--save",
        type=check_path,
        metavar="PATH",
        help="save json to given path",
    )
    parser.add_argument(
        "-s",
        "--save",
        type=check_path,
        metavar="PATH",
        help="save json to given path",
    )
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        default="https://jason.co.jp/network",
        metavar="URL",
        help="target url",
    )
    parser.add_argument("-V", "--version", action="version", version=__version__)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = get(args.url)
    if source is None:
        raise ValueError(f"Failed to fetch source from {args.url}")
    data = parse(source)
    json_str = json.dumps(data, indent=args.indent, ensure_ascii=False)
    if args.save:
        if os.path.exists(args.save) and not args.overwrite:
            print(
                "'{args.save}' already exists. Specify `-O` to overwrite.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(json_str, file=open(args.save, "w"))
    else:
        print(json_str)


if __name__ == "__main__":
    main()
