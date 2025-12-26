# Copyright (©) 2025, Alexander Suvorov. All rights reserved.
import json
import os
from datetime import datetime
from typing import Any, Dict, Optional
import uuid


def generate_id() -> str:
    return str(uuid.uuid4())


def format_datetime(dt: Optional[datetime] = None) -> str:
    if dt is None:
        dt = datetime.now()
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str)


def ensure_directory(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def load_json(filepath: str) -> Dict[str, Any]:
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_json(filepath: str, data: Dict[str, Any]):
    ensure_directory(filepath)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False, sort_keys=True)


def calculate_progress(total: int, completed: int) -> float:
    if total == 0:
        return 0.0
    return (completed / total) * 100
