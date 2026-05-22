import importlib.metadata
from pathlib import Path

try:
    __version__ = importlib.metadata.version("antigravityd")
except importlib.metadata.PackageNotFoundError:
    try:
        import tomllib

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        with open(pyproject_path, "rb") as f:
            __version__ = tomllib.load(f)["project"]["version"]
    except Exception:
        __version__ = "0.1.0"
