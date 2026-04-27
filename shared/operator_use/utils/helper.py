from pathlib import Path
import os

def is_binary_file(path: Path) -> bool:
 try:
 with open(path, "rb") as f:
 chunk = f.read(1024)
 return b"\x00" in chunk
 except(OSError, IOError):
 return False

def resolve(base: str | Path, path: str | Path) -> Path:
 path = Path(path)
 if path.is_absolute():
 return path.resolve()
 return Path(base).joinpath(path).resolve()

def ensure_directory(path: str) -> str:
 os.makedirs(path, exist_ok=True)
 return path
