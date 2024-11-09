"""Main module."""

from __future__ import annotations

import json
import sys

from .types import Args
from .utils import get, parse


def parse_args(args: list[str] = sys.argv[1:]) -> Args:
    """Parse arguments."""
    return Args().parse_args(args)


def main() -> None:
    """Execute command with argument."""
    args = parse_args()
    source = get(args.url)
    if source is None:
        msg = f"Failed to fetch source from {args.url}"
        raise ValueError(msg)
    data = parse(source)
    json_str = json.dumps(data, indent=args.indent, ensure_ascii=False)
    if not args.save:
        print(json_str)  # noqa: T201
        sys.exit(0)
    if args.save.is_file() and not args.overwrite:
        print(  # noqa: T201
            "'{args.save}' already exists. Specify `-O` to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)
    print(json_str, file=args.save.open("w"))


if __name__ == "__main__":
    main()
