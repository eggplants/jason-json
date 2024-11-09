"""Tests for `jason_json` package."""

from pathlib import Path

import pytest

from jason_json import __version__
from jason_json.main import main


def test_version() -> None:
    """Test version."""
    assert __version__ is not None


def test_cli_no_args(capfd: pytest.CaptureFixture[str]) -> None:
    """Test CLI with no arguments."""
    with pytest.raises(SystemExit) as e:
        main(test_args=[])
    assert e.value.args[0] == 0
    captured = capfd.readouterr()
    assert captured.out.startswith('{\n  "東京都": [')
    assert captured.out.endswith("    }\n  ]\n}\n")
    assert not captured.err


def test_cli_write_file(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    """Test CLI with write file."""
    path = tmp_path / "hoge"
    main(test_args=["-s", str(path)])
    captured = capfd.readouterr()
    assert not captured.out
    assert not captured.err

    with pytest.raises(SystemExit) as e:
        main(test_args=["--save", str(path)])
    assert e.value.args[0] == 1
    captured = capfd.readouterr()
    assert not captured.out
    assert captured.err == f"'{path}' already exists. Specify `-O` to overwrite.\n"

    main(test_args=["--save", str(path), "--overwrite"])
    captured = capfd.readouterr()
    assert not captured.out
    assert not captured.err
    assert path.open("r").read().startswith('{\n  "東京都": [')
    assert path.open("r").read().endswith("    }\n  ]\n}\n")


def test_cli_empty_output_path(capfd: pytest.CaptureFixture[str]) -> None:
    """Test CLI with empty output path."""
    with pytest.raises(SystemExit) as e:
        main(test_args=["--save"])
    assert e.value.args[0] == 2  # noqa: PLR2004
    captured = capfd.readouterr()
    assert not captured.out
    assert "expected one argument" in captured.err


def test_cli_output_path_is_dir(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    """Test CLI with output path is a directory."""
    with pytest.raises(SystemExit) as e:
        main(test_args=["--save", str(tmp_path)])
    assert e.value.args[0] == 1
    captured = capfd.readouterr()
    assert not captured.out
    assert f"'{tmp_path}' is not a file.\n" in captured.err
