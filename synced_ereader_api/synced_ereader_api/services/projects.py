# services/projects.py  (pure service)
from pathlib import Path
from typing import List


def create_project(base_dir: Path, name: str) -> str:
    if not name or not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Invalid project name.")

    target = (base_dir / name).resolve()

    try:
        target.mkdir(exist_ok=False)
    except FileExistsError as e:
        raise e
    except OSError as e:
        raise e

    return name

def list_projects(base_dir: Path) -> List[str]:
    base = base_dir.resolve()
    names = [p.name for p in base.iterdir() if p.is_dir()]
    return names