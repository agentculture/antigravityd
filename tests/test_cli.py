import importlib
import importlib.metadata
import sys

import pytest

from antigravityd import __version__
from antigravityd.cli import main


def test_version():
    assert __version__ == "0.1.0"


def test_cli_help(capsys):
    ret = main([])
    captured = capsys.readouterr()
    assert "Antigravity daemon" in captured.out
    assert ret == 0


def test_cli_serve(capsys):
    ret = main(["serve"])
    captured = capsys.readouterr()
    assert "Starting antigravityd daemon on port 8080" in captured.out
    assert ret == 0


def test_cli_serve_custom_port(capsys):
    ret = main(["serve", "--port", "9090"])
    captured = capsys.readouterr()
    assert "Starting antigravityd daemon on port 9090" in captured.out
    assert ret == 0


def test_cli_version(capsys):
    with pytest.raises(SystemExit):
        main(["--version"])
    captured = capsys.readouterr()
    assert (
        f"antigravityd {__version__}" in captured.out
        or f"antigravityd {__version__}" in captured.err
    )


def test_cli_no_args(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["antigravityd", "serve", "--port", "7777"])
    ret = main()
    captured = capsys.readouterr()
    assert "Starting antigravityd daemon on port 7777" in captured.out
    assert ret == 0


def test_package_not_found_error(monkeypatch):
    def mock_version(name):
        raise importlib.metadata.PackageNotFoundError

    monkeypatch.setattr(importlib.metadata, "version", mock_version)

    if "antigravityd" in sys.modules:
        sys.modules.pop("antigravityd")
    if "antigravityd.cli" in sys.modules:
        sys.modules.pop("antigravityd.cli")

    import antigravityd

    assert antigravityd.__version__ == "0.1.0"

    # Reload original so that later tests run cleanly
    monkeypatch.undo()
    if "antigravityd" in sys.modules:
        sys.modules.pop("antigravityd")
    if "antigravityd.cli" in sys.modules:
        sys.modules.pop("antigravityd.cli")
