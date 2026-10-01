import os
from pathlib import Path


def load_local_env() -> None:
    backend_dir = Path(__file__).resolve().parents[1]
    for env_path in (backend_dir / ".env", backend_dir.parent / ".env"):
        if not env_path.is_file():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip().strip('"').strip("'")
            if name and value and name not in os.environ:
                os.environ[name] = value


load_local_env()