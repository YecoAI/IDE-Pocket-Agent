from pathlib import Path

_DIR = Path.home() / ".operator-use"

def get_userdata_dir() -> Path:
 return _DIR

def get_workspaces_dir() -> Path:
 return _DIR / "workspaces"

def get_named_workspace_dir(name: str) -> Path:
 return get_workspaces_dir() / name

def get_media_dir() -> Path:
 return _DIR / "media"
