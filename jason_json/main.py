"""Main module."""

from __future__ import annotations

import json
import sys

from .model_types import Args
from .utils import get, parse


def parse_args(test_args: list[str] | None = None) -> Args:
    """Parse arguments.

    Args:
        test_args (list[str] | None): Arguments to parse. If None, use sys.argv[1:].

    Returns:
        Args: Parsed arguments.
    """
    if test_args is None:
        return Args().parse_args()
    return Args().parse_args(test_args)


def main(test_args: list[str] | None = None) -> None:
    """Execute command with argument.

    Args:
        test_args (list[str] | None): Arguments to parse. If None, use sys.argv[1:].
    """
    args = parse_args(test_args)
    source = get(args.url)
    if source is None:
        msg = f"Failed to fetch source from {args.url}"
        raise ValueError(msg)
    data = parse(source)
    if not args.save:
        print(json.dumps(data, indent=args.indent, ensure_ascii=False))  # noqa: T201
        sys.exit(0)
    if args.save is not None and args.save.exists() and not args.save.is_file():
        print(  # noqa: T201
            f"'{args.save}' is not a file.",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.save is not None and args.save.is_file() and not args.overwrite:
        print(  # noqa: T201
            f"'{args.save}' already exists. Specify `-O` to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.save is not None:
        with args.save.open("w", encoding="utf-8", errors="ignore") as f:
            json.dump(data, f, indent=args.indent, ensure_ascii=False)


if __name__ == "__main__":
    main()
